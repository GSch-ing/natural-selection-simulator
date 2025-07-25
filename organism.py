import pygame
import random

class Organism:
    def __init__(self, x, y, color, speed=3, energy=1.0, size=20, vision_radius=100):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.energy = energy
        self.size = size
        self.vision_radius = vision_radius

        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)

    def find_closest_food(self, foods):
        closest_food = None
        min_dist = float('inf')
        for food in foods:
            dist = ((self.x - food.x)**2 + (self.y - food.y)**2)**0.5
            if dist < self.vision_radius and dist < min_dist:
                min_dist = dist
                closest_food = food
        return closest_food

    def move(self, width, height, foods=None):
        target_food = None
        if foods:
            target_food = self.find_closest_food(foods)

        if target_food:
            # Mover hacia la comida
            dir_x = target_food.x - self.x
            dir_y = target_food.y - self.y
            mag = (dir_x**2 + dir_y**2)**0.5
            if mag != 0:
                dir_x /= mag
                dir_y /= mag

            self.x += dir_x * self.speed
            self.y += dir_y * self.speed

            # Actualizar direccion para suavizar movimiento cuando no haya comida
            self.dx = dir_x
            self.dy = dir_y
        else:
            # Movimiento aleatorio con direccion acumulativa
            self.dx += random.uniform(-0.2, 0.2)
            self.dy += random.uniform(-0.2, 0.2)
            mag = (self.dx**2 + self.dy**2)**0.5
            if mag != 0:
                self.dx /= mag
                self.dy /= mag

            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

        # Limitar dentro de la pantalla
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Reducir energia
        self.energy -= 0.001
        if self.energy < 0:
            self.energy = 0

    def draw(self, surface, bg_color, vision_radius=None):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        inner_radius = int(self.size * (1 - self.energy))
        if inner_radius > 0:
            pygame.draw.circle(surface, bg_color, (int(self.x), int(self.y)), inner_radius)
        if vision_radius:
            pygame.draw.circle(surface, (100, 100, 255), (int(self.x), int(self.y)), vision_radius, 1)
