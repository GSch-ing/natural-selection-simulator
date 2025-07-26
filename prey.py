import pygame
import math
import random
from organism import Organism

class Prey(Organism):
    def __init__(self, x, y, color, mutations=None):
        super().__init__(x, y, color, speed=2.0, vision=100, mutations=mutations)
        self.food_counter = 5  # comidas necesarias para reproducirse
        self.size = 8  # tamaño fijo, ya no hay niveles

    def move_towards_food(self, foods, predators, width, height):
        # Detectar depredador más cercano
        nearest_pred = None
        min_dist_pred = self.vision
        for predator in predators:
            dist = math.hypot(self.x - predator.x, self.y - predator.y)
            if dist < min_dist_pred:
                min_dist_pred = dist
                nearest_pred = predator

        # Radio dinámico de peligro
        danger_radius = self.vision * 0.6
        escaping = False

        # Detectar comida más cercana
        nearest_food = None
        min_dist_food = self.vision
        for food in foods:
            dist_food = math.hypot(self.x - food.x, self.y - food.y)
            if dist_food < min_dist_food:
                min_dist_food = dist_food
                nearest_food = food

        # Estrategia: si hay depredador cerca, huir; pero si hay comida MUY cerca, priorizar comida
        if nearest_pred and min_dist_pred < danger_radius:
            # Si hay comida extremadamente cerca (20 px) y el depredador no está encima (40 px), intenta comer
            if nearest_food and min_dist_food < 20 and min_dist_pred > 40:
                dx = nearest_food.x - self.x
                dy = nearest_food.y - self.y
                escaping = False
            else:
                # Huir del depredador
                dx = self.x - nearest_pred.x
                dy = self.y - nearest_pred.y
                escaping = True
        else:
            # Si no hay depredador peligroso, buscar comida
            if nearest_food:
                dx = nearest_food.x - self.x
                dy = nearest_food.y - self.y
            else:
                # Movimiento aleatorio
                self.move_random(width, height)
                return  # ya se movió

        # Normalizar dirección
        length = math.hypot(dx, dy)
        if length != 0:
            self.direction = [dx / length, dy / length]

        # Aplicar velocidad (más rápida si huye)
        move_speed = self.speed * (1.3 if escaping else 1.0)
        self.x += self.direction[0] * move_speed
        self.y += self.direction[1] * move_speed

        # Limitar bordes
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Gasto energético (huir gasta más)
        energy_cost = 0.004 if escaping else 0.003
        self.energy -= energy_cost * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

    def reproduce(self, mutation_chance=0.6):
        """Genera un nuevo Prey con posibles mutaciones."""
        new_mutations = set(self.mutations)

        # Posible mutación nueva
        if random.random() < mutation_chance:
            possible = ['red', 'blue', 'green']
            available = [m for m in possible if m not in new_mutations]
            if available:
                new_mutations.add(random.choice(available))

        child_color = self.mix_colors()

        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        return Prey(self.x + offset_x, self.y + offset_y, child_color, mutations=new_mutations)

    def draw(self, screen):
        fill_radius = int(self.size * self.energy)
        if fill_radius > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), fill_radius)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 2)
        self.draw_vision(screen)





