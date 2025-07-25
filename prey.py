import pygame
import math
import random
from organism import Organism

class Prey(Organism):
    def __init__(self, x, y, color, mutations=None):
        super().__init__(x, y, color, speed=2.0, vision=100, mutations=mutations)
        self.food_counter = 5  # comidas necesarias para reproducirse

    def move_towards_food(self, foods, predators, width, height):
        # 1) Buscar depredador más cercano en rango de visión
        threat = None
        min_dist_threat = self.vision
        for predator in predators:
            dist_pred = math.hypot(self.x - predator.x, self.y - predator.y)
            if dist_pred < min_dist_threat:
                min_dist_threat = dist_pred
                threat = predator

        if threat:
            # Huir del depredador
            dx = self.x - threat.x
            dy = self.y - threat.y
            length = math.hypot(dx, dy)
            if length != 0:
                self.direction = [dx / length, dy / length]
        else:
            # 2) Buscar comida si no hay depredador cerca
            target = None
            min_dist_food = self.vision
            for food in foods:
                dist_food = math.hypot(self.x - food.x, self.y - food.y)
                if dist_food < min_dist_food:
                    min_dist_food = dist_food
                    target = food

            if target:
                dx = target.x - self.x
                dy = target.y - self.y
                length = math.hypot(dx, dy)
                if length != 0:
                    self.direction = [dx / length, dy / length]
            else:
                # Movimiento aleatorio si no hay comida visible
                self.move_random(width, height)
                return  # ya se movió y gastó energía

        # Aplicar movimiento (huida o búsqueda de comida)
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Limitar bordes
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Gasto energético proporcional al nivel y mutaciones
        self.energy -= 0.001 * self.size_level * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

    def reproduce(self, mutation_chance=0.3):
        """
        Genera un nuevo Prey con mutaciones heredadas y posible mutación nueva.
        """
        # Heredar mutaciones del padre
        new_mutations = set(self.mutations)

        # Posibilidad de mutación nueva
        if random.random() < mutation_chance:
            possible = ['red', 'blue', 'green']
            available = [m for m in possible if m not in new_mutations]
            if available:
                new_mutations.add(random.choice(available))

        # Determinar color mezclado según mutaciones
        child_color = self.mix_colors()

        # Posición cercana al progenitor
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)

        return Prey(self.x + offset_x, self.y + offset_y, child_color, mutations=new_mutations)

    def draw(self, screen):
        # Dibujar relleno proporcional a la energía
        fill_radius = int(self.size * self.energy)
        if fill_radius > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), fill_radius)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 2)

        # Dibujar visión
        self.draw_vision(screen)






