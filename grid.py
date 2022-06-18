import pygame.surface


class Grid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.surface = pygame.surface.Surface((x * size + 1, y * size + 1)).convert_alpha()
        self.cache()

    def cache(self):
        self.surface.fill((0, 0, 0, 0))
        for x in range(0, self.x * self.size, self.size):
            pygame.draw.line(self.surface,
                             color="green",
                             start_pos=(x, 0),
                             end_pos=(x, self.y * self.size))
        for y in range(0, self.y * self.size, self.size):
            pygame.draw.line(self.surface,
                             color="green",
                             start_pos=(0, y),
                             end_pos=(self.x * self.size, y))

    def draw(self, screen: pygame.surface.Surface, pos):
        screen.blit(self.surface, pos)
