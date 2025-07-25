import pygame
import math
import random
from organism import Organism

class Predator(Organism):
    def __init__(self, x, y):
        # Siempre color rojo y sin mutaciones
        super().__init__(x, y, (255, 0, 0), speed=2.2, vision=120, mutations=None)
        self.food_counter = 5  # Más difícil reproducirse que presas

    def move_towards_prey(self, preys, width, height):
        # Buscar presa en rango de visión
        target = None
        min_dist = self.vision
        for prey in preys:
            # No puede cazar presas de mayor nivel
            if prey.size_level > self.size_level:
                continue
            dist = math.hypot(self.x - prey.x, self.y - prey.y)
            if dist < min_dist:
                min_dist = dist
                target = prey

        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            length = math.hypot(dx, dy)
            if length != 0:
                self.direction = [dx / length, dy / length]
        else:
            self.move_random(width, height)
            return

        # Aplicar movimiento hacia la presa
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Limitar bordes
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Gasto energético
        self.energy -= 0.001 * self.size_level * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

    def reproduce(self):
        """
        Genera un nuevo Predator nivel 1, siempre rojo y sin mutaciones.
        """
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        return Predator(self.x + offset_x, self.y + offset_y)

    def draw(self, screen):
        # Dibujar rombo relleno según energía
        fill_size = int(self.size * self.energy)
        if fill_size > 0:
            points_fill = [
                (self.x, self.y - fill_size),
                (self.x + fill_size, self.y),
                (self.x, self.y + fill_size),
                (self.x - fill_size, self.y)
            ]
            pygame.draw.polygon(screen, (255, 0, 0), points_fill)

        # Dibujar borde del rombo
        points_outline = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y)
        ]
        pygame.draw.polygon(screen, (255, 0, 0), points_outline, 2)

        # Dibujar visión
        self.draw_vision(screen)


