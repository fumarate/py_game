import pygame
from enum import Enum


class Sound:
    class SoundEnum(Enum):
        SELECT = (0, "res/select.wav")
        READY = (1, "res/ready.wav")
        EXTEND = (2, "res/extend.wav")
        SELL = (3, "res/sell.wav")
        EXPLODE = (4, "res/explode.wav")
        END = (5, "res/end.wav")
        BOUGHT = (6, "res/bought.wav")
        GOT = (7, "res/got.wav")
        GOT_GOOD = (8, "res/got_good.wav")
        GOT_BAD = (9, "res/got_bad.wav")
        DRAG = (10, "res/drag.wav")

    @staticmethod
    def play(sound_id: SoundEnum, loop=False):
        pygame.mixer.Sound(sound_id.value[1]).play(loops=0 if not loop else -1)

    @staticmethod
    def stop():
        pygame.mixer.stop()
