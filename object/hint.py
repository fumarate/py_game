import pygame.sprite


class Hint(pygame.sprite.Sprite):
    def __init__(self, hint: any, size: int, pos: tuple, color="#000000", bg_color="#FFFFFF", head="", tail=""):
        super().__init__()
        self.pos = pos
        self.speed = .005
        self.scale = 1
        self.size = size
        self.original_image = pygame.font.Font("res/font.ttf", size).render(head + str(hint) + tail, True, color,
                                                                            bg_color).convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.original_image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.head = head
        self.tail = tail
        self.color = color
        self.bg_color = bg_color
        self.max_scale = 2

    def change(self, hint_str):
        self.original_image = pygame.font.Font("res/font.ttf", self.size).render(self.head + str(hint_str) + self.tail,
                                                                          True, self.color,
                                                                          self.bg_color).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (
            self.scale * self.original_image.get_width(), self.scale * self.original_image.get_height()))

    def update(self):
        self.scale += self.speed
        if self.scale <= self.max_scale:
            self.image = pygame.transform.scale(self.original_image, (
                self.scale * self.original_image.get_width(), self.scale * self.original_image.get_height()))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.pos
        else:
            if self.scale - self.max_scale >= 2:
                self.kill()
