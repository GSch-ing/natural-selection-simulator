import pygame
import random
import math

class Organism:
    def __init__(self, x, y, color, speed=2.0, vision=100, mutations=None):
        self.x = x
        self.y = y

        # Tamaño fijo (sin niveles ahora)
        self.size = 10

        # Atributos base
        self.base_speed = speed
        self.base_vision = vision
        self.speed = speed
        self.vision = vision
        self.energy = 0.6  # energía inicial

        # Mutaciones
        self.mutations = mutations if mutations else set()
        self.color = color

        # Dirección inicial aleatoria
        self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]

        # Factor de consumo energético
        self.energy_cost_factor = 1.0
        self.apply_mutations()

    # -------------------
    # Movimiento aleatorio
    # -------------------
    def move_random(self, width, height):
        self.direction[0] += random.uniform(-0.2, 0.2)
        self.direction[1] += random.uniform(-0.2, 0.2)

        # Normalizar
        length = math.hypot(*self.direction)
        if length != 0:
            self.direction[0] /= length
            self.direction[1] /= length

        # Mover
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Limitar bordes
        self.stay_within_bounds(width, height)

        # Consumir energía (centralizado)
        self.consume_energy()

    # -------------------
    # Consumo energético
    # -------------------
    def consume_energy(self):
        # Ajustás este valor para que mueran más rápido o más lento
        self.energy -= 0.0001 * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

    # -------------------
    # Mutaciones
    # -------------------
    def apply_mutations(self):
        """Ajusta velocidad, visión y gasto según mutaciones activas."""
        # Reset stats base
        self.speed = self.base_speed
        self.vision = self.base_vision
        energy_factor = 1.0

        # Rojo: +20% velocidad, +20% consumo
        if 'red' in self.mutations:
            self.speed *= 1.3
            energy_factor *= 1.3

        # Azul: +30% visión, -10% velocidad
        if 'blue' in self.mutations:
            self.vision *= 1.8
            self.speed *= 0.8

        # Verde: -20% consumo, -10% velocidad
        if 'green' in self.mutations:
            energy_factor *= 0.6
            self.speed *= 0.8

        self.energy_cost_factor = energy_factor
        self.color = self.mix_colors()

    def mix_colors(self):
        """Combina colores según mutaciones presentes."""
        base_colors = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0)
        }
        r, g, b = 0, 0, 0
        for m in self.mutations:
            cr, cg, cb = base_colors[m]
            r = min(255, r + cr)
            g = min(255, g + cg)
            b = min(255, b + cb)
        return (r, g, b) if self.mutations else (200, 200, 200)

    # -------------------
    # Visión (debug visual)
    # -------------------
    def draw_vision(self, screen):
        pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), int(self.vision), 1)

    # -------------------
    # Reproducción genérica
    # -------------------
    def reproduce(self, mutation_chance=0.3):
        """Genera un nuevo organismo con posibles mutaciones heredadas."""
        new_mutations = set(self.mutations)

        # Probabilidad de mutación nueva
        if random.random() < mutation_chance:
            possible = ['red', 'blue', 'green']
            available = [m for m in possible if m not in new_mutations]
            if available:
                new_mutations.add(random.choice(available))

        # Posición cercana
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)

        return self.__class__(self.x + offset_x, self.y + offset_y, self.mix_colors(), mutations=new_mutations)
    
    def stay_within_bounds(self, width, height):
        """Mantiene al organismo dentro de los límites y lo hace rebotar hacia adentro."""
        bounced = False

        # Chequeo en X
        if self.x < self.size:
            self.x = self.size
            self.direction[0] = abs(self.direction[0])  # rebota hacia la derecha
            bounced = True
        elif self.x > width - self.size:
            self.x = width - self.size
            self.direction[0] = -abs(self.direction[0])  # rebota hacia la izquierda
            bounced = True

        # Chequeo en Y
        if self.y < self.size:
            self.y = self.size
            self.direction[1] = abs(self.direction[1])  # rebota hacia abajo
            bounced = True
        elif self.y > height - self.size:
            self.y = height - self.size
            self.direction[1] = -abs(self.direction[1])  # rebota hacia arriba
            bounced = True

        # Si rebotó, normalizamos dirección
        if bounced:
            length = math.hypot(*self.direction)
            if length != 0:
                self.direction[0] /= length
                self.direction[1] /= length


