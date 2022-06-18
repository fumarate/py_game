import json
import sys
from copy import copy, deepcopy
import weakref
import pygame

from object.object import MineSprite
from resource import Resource

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("GoldMiner")
    bg_img = pygame.image.load("res/background.jpg").convert()
    bg_img = pygame.transform.scale(bg_img, (1280, 720))
    prefabs = Resource.get_prefab()
    x_pos = 0
    for obj in prefabs:
        obj.rect.x, obj.rect.y = x_pos, 800
        x_pos += (obj.width + 20)
    prefabs_group = pygame.sprite.Group()
    prefabs_group.add(prefabs)
    map_group = pygame.sprite.Group()
    dragging_obj = None
    while True:
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(dragging_obj is None)
                if  dragging_obj is None:
                    # 判断指针落在地图还是物品栏
                    pointer_sprite = pygame.sprite.Sprite()
                    pointer_sprite.image = pygame.surface.Surface((1, 1))
                    pointer_sprite.rect = pointer_sprite.image.get_rect()
                    pointer_sprite.rect.x, pointer_sprite.rect.y = mpos
                    if mpos[1] >= 720:
                        # 在物品栏
                        if o := pygame.sprite.spritecollide(pointer_sprite, prefabs_group, False):
                            # 抓住物品
                            dragging_obj = Resource.get_prefab(o[0].name)
                    else:
                        if o := pygame.sprite.spritecollide(pointer_sprite, map_group, False):
                            # 抓住物品
                            dragging_obj = o[0]
                else:
                    if  mpos[1]<=720 and dragging_obj is not None:
                        map_group.add(dragging_obj)
                        dragging_obj =None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    map_json = {"map":{
                        "target":650,
                        "objects":[]
                    }}
                    for mine in map_group:
                        map_json["map"]["objects"].append(
                            {
                                "type": mine.name,
                                "x": mine.rect.x,
                                "y": mine.rect.y
                            }
                        )
                    import easygui as g
                    target_path = g.filesavebox("save map json")
                    with open(target_path,mode= "w+",encoding="UTF-8") as map_file:
                        json.dump(map_json,map_file,indent=2)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(bg_img, (0, 0))
        screen.blit(pygame.surface.Surface((1280,240)),(0,720))
        pos = 0
        prefabs_group.draw(screen)
        map_group.draw(screen)
        if dragging_obj is not None:
            dragging_obj.rect.x, dragging_obj.rect.y = mpos[0]-dragging_obj.width/2,mpos[1]-dragging_obj.height/2
            screen.blit(dragging_obj.image, dragging_obj.rect)
        pygame.display.flip()
