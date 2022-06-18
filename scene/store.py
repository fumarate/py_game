import numpy as np
import pygame

from constrant import SceneCode
from resource import Resource
from scene.scene import Scene
from scene.ui import Button
from sound import Sound


class Store(Scene):
    def __init__(self, manager, player):
        super().__init__(manager)
        self.player = player
        self.store_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(Button(Resource.get_text("下一关", 50), (100, 100), self.end))
        goods = ["bomb_s", "power", "lucky", "stone_book", "diamond_wash"]
        self.values = [None for _ in goods]
        self.selected = -1
        self.hint = ""
        for i, b in enumerate(np.random.randint(0, 2, len(goods))):
            if b == 1:
                good = Resource.get_prefab(goods[i])
                good.rect.x, good.rect.y = (160 * i + 80, 360)
                self.store_group.add(good)
                self.values[i] = good.value

    def produce(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            pointer_sprite = pygame.sprite.Sprite()
            pointer_sprite.image = pygame.surface.Surface((1, 1))
            pointer_sprite.rect = pointer_sprite.image.get_rect()
            pointer_sprite.rect.x, pointer_sprite.rect.y = pygame.mouse.get_pos()
            if o := pygame.sprite.spritecollide(pointer_sprite, self.store_group, False):
                if o[0].value <= self.player.money:
                    self.player.money -= o[0].value
                    o[0].kill()
                    Sound.play(Sound.SoundEnum.BOUGHT)
                    if o[0].name == "bomb_s":
                        self.player.bomb += 1
                        self.values[0] = None
                    elif o[0].name == "power":
                        self.player.power = 2
                        self.values[1] = None
                    elif o[0].name == "lucky":
                        self.player.lucky = 1
                        self.values[2] = None
                    elif o[0].name == "stone_book":
                        self.player.stone = 1
                        self.values[3] = None
                    elif o[0].name == "diamond_wash":
                        self.player.diamond = 1
                        self.values[4] = None
            elif o := pygame.sprite.spritecollide(pointer_sprite, self.ui_group, False):
                o[0].call()

    def update(self):
        pointer_sprite = pygame.sprite.Sprite()
        pointer_sprite.image = pygame.surface.Surface((1, 1))
        pointer_sprite.rect = pointer_sprite.image.get_rect()
        pointer_sprite.rect.x, pointer_sprite.rect.y = pygame.mouse.get_pos()
        if o := pygame.sprite.spritecollide(pointer_sprite, self.store_group, False):
            self.hint = o[0].comment
        return self

    def display(self, screen):
        screen.blit(pygame.transform.scale(pygame.image.load("res/store.jpg"), (1280, 720)), (0, 0))
        screen.blit(pygame.font.SysFont("Microsoft Yahei", 30).render(self.hint, True, "#000000", "#c48c2f"), (50, 550))
        screen.blit(Resource.get_text("金钱：$" + str(self.player.money), 50, "#00FF00", alpha=True), (70, 140))
        for i, x in enumerate(range(80, 880, 160)):
            if self.values[i] is not None:
                screen.blit(Resource.get_text(str(self.values[i]), 30, "#00FF00", alpha=True), (x, 480))
        self.store_group.draw(screen)
        self.ui_group.draw(screen)

    def end(self):
        self.manager.set_scene(SceneCode.PLAYING)
