import json

from client import MineClient
from object.hint import Hint
from scene.scene import Scene
from object.player import Player
from object.object import MineSprite
from object.hook import Hook
import pygame
from constrant import RESOLUTION, SceneCode
import sys
from resource import Resource
from sound import Sound

sys.path.append("..")


class Game(Scene):
    # 客户端Game类
    def __init__(self, client=None):
        # res
        # self.client  = MineClient()
        self.background = pygame.transform.scale(
            pygame.image.load("res/background.jpg").convert(), RESOLUTION)
        self.font = pygame.font.Font("res/font.ttf", 50)
        # status variable
        self.frame = 0
        self.pausing = False
        self.running = False
        self.total_time = 60
        self.target = 650
        # obj
        self.player = Player(self)
        self.mines = pygame.sprite.Group()
        self.load("123.json")
        self.hint_group = pygame.sprite.Group()
        self.money_hint = Hint(self.player.money, 50, (150, 10), head="$", color="#009900", bg_color="#FCCE33")
        self.money_hint.speed = 0
        self.hint_group.add(self.money_hint)
        self.target_hint = Hint(self.target, 50, (150, 70), head="$", color="#ff9900", bg_color="#FCCE33")
        self.target_hint.speed = 0
        self.hint_group.add(self.target_hint)

    def load(self, map_path: str):
        with open(map_path, mode="r+") as map_file:
            map_json = json.load(map_file)["map"]
            self.target = map_json["target"]
            for obj in map_json["objects"]:
                s_obj = Resource.get_prefab(obj["type"])
                self.put_obj(s_obj, (obj["x"], obj["y"]))

    def put_obj(self, obj: MineSprite, pos: tuple) -> None:
        obj.rect.x, obj.rect.y = pos
        self.mines.add(obj)

    def show_hint(self, hint_str: str):
        self.hint_group.add(Hint(hint_str, 20, (400, 10), head="$", color="#009900", bg_color="#FCCE33"))

    def start(self):
        self.running = True
        self.frame = 0

    def end(self):
        self.running = False
        self.manager.set_scene(SceneCode.AFTER)

    def produce(self, event: pygame.event.Event):
        """
        处理输入事件
        :param event:
        :return:
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.use_bomb()
                # self.client.send("key=w")
            if event.key == pygame.K_s:
                self.player.extend()
                # self.client.send("key=s")
            if event.key == pygame.K_2:
                self.pausing = not self.pausing
                # self.client.send("pause")

    def update(self):
        """
        同步服务端信息并更新
        :return:
        """
        self.frame += 1
        if self.running and not self.pausing:
            # object update
            self.money_hint.change(str(self.player.money))
            self.player.update()
            # 检查钩子状态
            if self.player.hook.out and self.player.hook.speed > 0:

                collided_mines = pygame.sprite.spritecollide(self.player.hook,
                                                             self.mines,
                                                             True,
                                                             collided=pygame.sprite.collide_circle)
                if collided_mines not in [None, []]:
                    cm_tags = collided_mines[0].tags
                    if "good" in cm_tags:
                        Sound.play(Sound.SoundEnum.GOT_GOOD)
                    elif "bad" in cm_tags:
                        Sound.play(Sound.SoundEnum.GOT_BAD)
                    else:
                        Sound.play(Sound.SoundEnum.GOT)
                    self.player.hook.carry(collided_mines[0])

            FPS = 60
            if self.frame / FPS >= self.total_time:
                self.end()
            self.hint_group.update()
        return self

    # 暴露在外的方法

    @property
    def last_time(self):
        FPS = 60
        return int(self.total_time - self.frame / FPS)

    def display(self, screen):
        # 显示背景
        screen.blit(self.background, (0, 0))
        # 积分器
        screen.blit(self.font.render("金钱；", True, "#8F6E06", "#FCCE33"), (10, 10))
        screen.blit(self.font.render("目标；", True, "#8F6E06", "#FCCE33"), (10, 70))
        screen.blit(self.font.render(str(self.last_time),
                                     True, "#8F6E06", "#FCCE33"), (800, 10))



        self.hint_group.draw(screen)
        self.mines.draw(screen)
        self.player.draw(screen)
        screen.blit(self.player.get_panel(), (0, 570))
