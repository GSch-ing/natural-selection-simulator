import pygame
import math
import random
from organism import Organism

class Predator(Organism):
    def __init__(self, x, y):
        # Color rojo, sin mutaciones, visión aumentada
        super().__init__(x, y, (255, 140, 0), speed=2.0, vision=140, mutations=None)
        self.food_counter = 5

    def move_towards_prey(self, preys, width, height):
        # Buscar presa en rango de visión
        target = None
        min_dist = self.vision
        for prey in preys:
            dist = math.hypot(self.x - prey.x, self.y - prey.y)
            if dist < min_dist:
                min_dist = dist
                target = prey

        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            length = math.hypot(dx, dy)
            if length != 0:
                # Boost de velocidad al perseguir presa
                boosted_speed = self.speed * 1.4
                self.direction = [dx / length, dy / length]
                self.x += self.direction[0] * boosted_speed
                self.y += self.direction[1] * boosted_speed
        else:
            # Movimiento aleatorio con menor gasto energético
            self.move_random(width, height)
            return

        # Limitar bordes
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Gasto energético reducido para mayor supervivencia
        self.energy -= 0.002 * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

    def reproduce(self, prey_count):
        # Reproducción dinámica: si hay más presas que depredadores, puede reproducirse
        if prey_count > 0 and prey_count > 1:
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            return Predator(self.x + offset_x, self.y + offset_y)
        else:
            return None

    def draw(self, screen):
        fill_size = int(self.size * self.energy)
        if fill_size > 0:
            points_fill = [
                (self.x, self.y - fill_size),
                (self.x + fill_size, self.y),
                (self.x, self.y + fill_size),
                (self.x - fill_size, self.y)
            ]
            pygame.draw.polygon(screen, (255, 140, 0), points_fill)

        points_outline = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y)
        ]
        pygame.draw.polygon(screen, (255, 140, 0), points_outline, 2)

        self.draw_vision(screen)




