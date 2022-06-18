from math import sin, cos, pi

import pygame
from typing import NewType

from sound import Sound
from .object import MineSprite
from .bomb import BombSprite

Hook = NewType("Hook", object)
ROPE_MIN_LENGTH = 40
ROPE_MAX_LENGTH = 800
HOOK_OUT_SPEED = 3
HOOK_BACK_SPEED = -5
HOOK_HORI_SPEED = 0.015


class Hook(pygame.sprite.Sprite):
    def __init__(self, player,pos=(640, 120), enable_ray=False):
        super().__init__()
        self.player = player
        self.game = self.player.game
        self.carrying_offset = None
        self.dir = pygame.math.Vector2(0, 1)
        self.carrying_object = None
        self.enable_ray = enable_ray
        self.th = 0
        self.pos = pos
        self.out = False
        self.speed = HOOK_OUT_SPEED
        self.r = ROPE_MIN_LENGTH
        self.a = 0
        self.speed_h = HOOK_HORI_SPEED
        self.origin_image_open = pygame.transform.rotate(pygame.image.load("res/hook_open.png"), 270)
        self.origin_image_close = pygame.transform.rotate(pygame.image.load("res/hook_close.png"), 270)
        self.rect = self.origin_image_open.get_rect()
        self.image = self.origin_image_open.copy()
        self.bomb = None
        self.speed_s = 0

    def update(self):
        if self.bomb is not None:
            self.bomb.update()
        if not self.out:
            # rolling
            self.a += self.speed_h
            self.th = sin(self.a) * pi / 2.5
            self.dir = pygame.math.Vector2(sin(self.th), cos(self.th)).normalize()
        else:
            # out
            if self.speed > 0:
                # down dir
                self.r += self.speed
                if self.r >= ROPE_MAX_LENGTH:
                    # reversing
                    self.speed = HOOK_BACK_SPEED
            else:
                # back
                if self.carrying_object is not None:
                    self.r += self.speed * self.player.power / self.carrying_object.mass
                else:
                    self.r += self.speed
                if self.r <= ROPE_MIN_LENGTH:
                    Sound.stop()
                    self.r = ROPE_MIN_LENGTH
                    self.out = False
                    self.speed = HOOK_OUT_SPEED
                    if self.carrying_object is not None:
                        self.player.sell(self.carrying_object)
                        self.carrying_object.kill()
                        self.carrying_object = None
        if self.carrying_object:
            self.image = pygame.transform.rotate(self.origin_image_close, self.th * 180 / pi)
            # 是否有夹住的物体，若有一并绘制
            self.carrying_object.rect.x, self.carrying_object.rect.y = self.rect.x + self.carrying_offset.x, self.rect.y + self.carrying_offset.y
        else:
            self.image = pygame.transform.rotate(self.origin_image_open, self.th * 180 / pi)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (
            self.end_pos[0] - self.rect.centerx,
            self.end_pos[1] - self.rect.centery)
        return self

    def extend(self):
        Sound.play(Sound.SoundEnum.EXTEND)
        self.out = True

    def carry(self, mine: MineSprite):
        Sound.play(Sound.SoundEnum.DRAG, loop=True)
        self.speed = HOOK_BACK_SPEED
        mine.dir = self.dir
        mine.speed = self.speed * self.player.power / mine.mass
        self.carrying_object = mine

        self.carrying_object.image = pygame.transform.rotate(self.carrying_object.image, self.th * 180 / pi)

        self.carrying_offset = self.dir * self.carrying_object.radius - pygame.math.Vector2(
            self.carrying_object.rect.w * 0.5, self.carrying_object.rect.h * 0.5)
    def use_bomb(self):
        if self.carrying_object is not None and self.bomb is None:
            self.bomb = BombSprite(self)

    def pause(self):
        self.speed_s, self.speed = self.speed, 0

    def resume(self):
        self.speed = self.speed_s

    @property
    def end_pos(self):
        return self.pos[0] + self.dir.x * self.r, self.pos[1] + self.dir.y * self.r

    def draw(self, screen):

        if self.carrying_object is not None:
            screen.blit(self.carrying_object.image, self.carrying_object.rect)
        # 绘制rope
        pygame.draw.line(screen, "black", self.pos, self.end_pos, width=3)
        # pygame.draw.rect(screen, "yellow", self.rect)
        # 绘制hook
        screen.blit(self.image, self.rect)
        if self.enable_ray:
            eep = (
                self.pos[0] + self.dir.x * (ROPE_MAX_LENGTH + 200),
                self.pos[1] + self.dir.y * (ROPE_MAX_LENGTH + 200))
            pygame.draw.line(screen, "red", self.pos, eep)
        if self.bomb is not None:
            screen.blit(self.bomb.image, self.bomb.rect)
