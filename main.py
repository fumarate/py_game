import pygame
import sys

from client import MineClient
from constrant import *
from scene import Store, Game, Start
from enum import Enum

"""
HOME->BEFORE->GAME->AFTER->STORE
"""


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(TITLE)
        self.scene_code = SceneCode.HOME
        game = Game()
        self.player = game.player
        self.scenes = [Start(self), None, game, None, Store(self, self.player)]

    def run(self):
        self.scene.start()
        fcclock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2]:
                    print(pygame.mouse.get_pos())
                else:
                    self.scene.produce(event)
            self.scene.update().display(self.screen)
            fcclock.tick(60)
            pygame.display.flip()

    def set_scene(self, scene_code):
        self.scene_code = scene_code
        self.scene.start()

    @property
    def scene(self):
        return self.scenes[self.scene_code.value]


if __name__ == "__main__":
    Main().run()
