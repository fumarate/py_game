import json
from functools import lru_cache

import pygame.image

from object import MineSprite

from typing import Union, List


class Resource:
    @staticmethod
    @lru_cache
    def get_image(name) -> pygame.surface.Surface:
        """
        图像加载器
        :param name: 图像资源名
        :return: Surface
        """
        return pygame.image.load("res/" + name)

    @staticmethod
    def get_text(text, size, color="#000000", bg_color="#FFFFFF", alpha=False):
        if alpha:
            return pygame.font.SysFont("Microsoft Yahei", size).render(text, True, color).convert_alpha()
        else:
            return pygame.font.SysFont("Microsoft Yahei", size).render(text, True, color, bg_color)

    @staticmethod
    def get_prefab(name: str = None) -> Union[MineSprite, List[MineSprite]]:
        """
        预制件加载器
        :param name: 预制件名字
        :return: 新的预制件Sprite对象或者所有预制件列表
        """
        if name is None:
            prefabs = []
            for obj in Resource.get_prefab_configuration():
                prefabs.append(Resource.get_prefab(obj["name"]))
            return prefabs
        else:
            obj = Resource.get_prefab_configuration(name=name)
            return MineSprite(Resource.get_image(obj["res"]), obj["name"], obj["tags"], obj["value"], obj["mass"],
                              obj["comment"])

    @staticmethod
    @lru_cache
    def get_prefab_configuration(name: str = None) -> dict:
        """
        预制件配置加载器
        :param name: 预制件名字
        :return: 预制件配置dict
        """
        with open("object/prefab.json", mode="r+", encoding="utf-8") as prefab_repo:
            prefab_json = json.load(prefab_repo)
            if name is None:
                return prefab_json["prefab"]
            for obj in prefab_json["prefab"]:
                if obj["name"] == name:
                    return obj
        raise Exception("该名称未找到")
