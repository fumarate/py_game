import pygame.sprite


class UI:
    def __init__(self):
        self.ui_group = pygame.sprite.Group()

    def check(self):
        pass


class Label(pygame.sprite.Sprite):
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


class Button(pygame.sprite.Sprite):
    def __init__(self,
                 surface: pygame.surface.Surface,
                 pos: tuple,
                 callback: callable,
                 callback_args: tuple = (),
                 callback_kwargs: dict = {},
                 name: str = None
                 ):
        """
        初始化按钮精灵。
        :param surface: 所使用的surface
        :param pos: 位置
        :param callback:回调函数
        :param callback_args: 回调函数的参数
        :param callback_kwargs: 回调函数的字典参数
        :param name: 按钮名字
        """
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.callback_kwargs = callback_kwargs
        self.callback_args = callback_args
        self.rect.x, self.rect.y = pos
        self.callback = callback
        self.name = name

    def call(self) -> any:
        """
        调用回调函数。
        :return: 回调函数的返回值
        """
        return self.callback(*self.callback_args, **self.callback_kwargs)
