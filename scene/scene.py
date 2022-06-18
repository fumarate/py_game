import pygame.surface


class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.ui_group = pygame.sprite.Group()

    def start(self):
        pass

    def produce(self, event: pygame.event.Event):
        if event.type ==pygame.MOUSEBUTTONDOWN:
            pointer_sprite = pygame.sprite.Sprite()
            pointer_sprite.image = pygame.surface.Surface((1, 1))
            pointer_sprite.rect = pointer_sprite.image.get_rect()
            pointer_sprite.rect.x, pointer_sprite.rect.y = pygame.mouse.get_pos()
            if o := pygame.sprite.spritecollide(pointer_sprite, self.ui_group, False):\
                o[0].call()
        return self

    def update(self):
        return self

    def display(self, screen: pygame.surface.Surface):
        pass

    def end(self):
        pass

    def switch_to(self, scene_code):
        print("jmp to"+str(scene_code) )
        self.manager.set_scene(scene_code)
