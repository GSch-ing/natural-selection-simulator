import pygame
import random

class Food:
    def __init__(self, x, y, size=8):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 200, 0)  # Verde

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    @staticmethod
    def spawn_random(width, height, margin=20):
        x = random.randint(margin, width - margin)
        y = random.randint(margin, height - margin)
        return Food(x, y)
