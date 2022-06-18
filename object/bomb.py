import pygame.sprite
from math import pi
from sound import Sound

class BombSprite(pygame.sprite.Sprite):
    def __init__(self, hook):
        super(BombSprite, self).__init__()
        self.hook = hook
        self.dir = hook.dir
        self.speed = 2000
        self.image = pygame.image.load("res/bomb.png")
        self.image = pygame.transform.rotate(self.image, hook.th * 180 / pi)
        self.rect = self.image.get_rect()
        self.start_pos = hook.pos[0] - self.rect.w / 2, hook.pos[1] - self.rect.h / 2
        self.frame = 0
        self.create_time = pygame.time.get_ticks()


    @property
    def pos(self):
        vec = (pygame.time.get_ticks() - self.create_time) / 1000 * self.speed * self.dir
        return vec.x + self.start_pos[0], vec.y + self.start_pos[1]

    def update(self):
        if self.frame != 0:
            # 已经爆炸
            self.frame += .3
            self.image = pygame.transform.scale(pygame.image.load("res/explode_%s.png" % str(int(self.frame)).zfill(2)),
                                                (self.hook.carrying_object.rect.w * 2,
                                                 self.hook.carrying_object.rect.h * 2))
            # 动画加载优化速度
            self.rect = self.image.get_rect()
            self.rect.x = self.hook.end_pos[0] - self.rect.w / 2
            self.rect.y = self.hook.end_pos[1] - self.rect.h / 2
            if self.frame >= 22:
                self.hook.bomb = None
                self.hook.carrying_object = None
                self.hook.r = 80
                self.hook.resume()
                return
        else:
            # 仍未爆炸
            self.rect.x, self.rect.y = self.pos
            if self.hook.carrying_object is not None and pygame.sprite.collide_mask(self, self.hook.carrying_object):
                self.frame += 1
                Sound.stop()
                Sound.play(Sound.SoundEnum.EXPLODE)
                self.hook.pause()
