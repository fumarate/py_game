import random

import pygame.surface
from typing import NewType, List, Union

MineSprite = NewType("MineSprite", object)

from math import sqrt


class MineSprite(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.surface.Surface,
                 name: str,
                 tags: List[str],
                 value: Union[int, List[int]],
                 mass: int,
                 comment: Union[str, None] = None):
        super().__init__()
        self.comment = comment
        self.tags = tags
        self.name = name
        self.image = surface
        if type(value) == list:
            self.value = random.randint(value[0], value[1])
        else:
            self.value = value
        self.mass = mass
        self.speed = 0
        self.rect = self.image.get_rect()
    @property
    def width(self):
        return self.rect.w

    @property
    def height(self):
        return self.rect.h

    @property
    def radius(self):
        return sqrt(self.width * self.height) / 2 * 0.8
    def update(self):
        pass


class AnimalSprite(MineSprite):
    pass
