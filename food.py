import pygame
import random

class Food:
    def __init__(self, x, y, size=4):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 255, 0)

    @classmethod
    def spawn_random(cls, width, height):
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)
        return cls(x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
