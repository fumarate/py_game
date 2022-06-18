import pygame.transform

from constrant import SceneCode
from resource import Resource
from scene.scene import Scene
from scene.ui import Button


class Start(Scene):
    def __init__(self, manager):
        super(Start, self).__init__(manager)
        start_btn = Button(Resource.get_text("开始游戏", color="#000000", alpha=True, size=30),
                           pos=(280, 150),
                           callback=self.switch_to,
                           callback_args=(SceneCode.PLAYING,)
                           )
        self.ui_group.add(start_btn)

    def display(self, screen):
        bg_img = pygame.transform.scale(pygame.image.load("res/start.jpg"), (1280, 720))
        screen.blit(bg_img, (0, 0))
        self.ui_group.draw(screen)
