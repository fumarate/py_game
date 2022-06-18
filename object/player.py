from math import pi

import pygame.sprite

from object.hook import Hook
from object.object import MineSprite
from resource import Resource
from sound import Sound


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.power = 1
        self.lucky = 0
        self.bomb = 0
        self.stone = 1
        self.diamond = 1
        self.money = 114514
        self.hook = Hook(self, enable_ray=True)

    @property
    def image(self):
        return self.hook.image

    @property
    def rect(self):
        return self.hook.rect

    def use_bomb(self):
        self.hook.use_bomb()

    def extend(self):
        self.hook.extend()

    def update(self):
        self.hook.update()

    def new(self):
        self.power = 0
        self.lucky = 0
        self.stone = 0
        self.diamond = 0

    def sell(self, obj: MineSprite):
        value = 0
        if "gold" in obj.tags:
            value += obj.value
        elif "stone" in obj.tags:
            value += obj.value * self.stone
        elif "diamond" in obj.tags:
            value += obj.value + 300
        elif "package" in obj.tags:
            import random
            res = random.randint(0, 100)
            if 0 <= res < 10:
                value += random.randint(0, 200)
            elif 10 <= res < 25:
                # 生力水
                pass
            elif 25 <= res < 70:
                # bomb
                pass
            elif 70 <= res <= 100:
                value += random.randint(100, 1000)
        self.money += value
        self.game.show_hint(str(value))
        del obj
        Sound.play(Sound.SoundEnum.BOUGHT)

    def get_panel(self):
        status_surface = pygame.surface.Surface((300, 150))
        status_surface.blit(Resource.get_text("力量：" + str(self.power), 20, "#00FF00", "#000000"), (0, 0))
        status_surface.blit(Resource.get_text("Hook radius:" + str(round(self.hook.r)), 20, "#00FF00", "#000000"),
                            (0, 30))
        status_surface.blit(Resource.get_text("Hook θ:" + str(self.hook.th * 180 / pi), 20, "#00FF00", "#000000"),
                            (0, 60))
        return status_surface

    def draw(self, screen):
        self.hook.draw(screen)
