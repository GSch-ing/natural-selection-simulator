import pygame
import random
import math

class Organism:
    def __init__(self, x, y, color, speed=2.0, vision=100, mutations=None):
        self.x = x
        self.y = y

        # ---- Niveles ----
        self.size_step = 10
        self.size_level = 1
        self.max_level = 6
        self.size = self.size_level * self.size_step

        # ---- Base Stats ----
        self.base_speed = speed
        self.base_vision = vision
        self.speed = speed
        self.vision = vision
        self.energy = 0.5  # 50% inicial

        # ---- Mutaciones ----
        self.mutations = mutations if mutations else set()
        self.color = color

        # Aplicar mutaciones iniciales
        self.apply_mutations()

        # ---- Dirección inicial aleatoria ----
        self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]

        # ---- Control de degradación de nivel ----
        self.recently_downgraded = False

    # -------------------
    # Movimiento y energía
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
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))

        # Gasto energético proporcional al nivel y mutaciones
        self.energy -= 0.001 * self.size_level * self.energy_cost_factor
        self.energy = max(0.0, self.energy)

        self.lower_if_low_energy()

    # -------------------
    # Crecimiento / Decrecimiento
    # -------------------
    def grow_if_ready(self):
        """
        Sube de nivel cuando energía >= 0.75, hasta máximo.
        Al crecer, gasta parte de la energía pero no queda vacío.
        """
        if self.energy >= 0.75 and self.size_level < self.max_level:
            self.size_level += 1
            self.size = self.size_level * self.size_step
            self.update_stats()

            # Tras subir, energía baja a 50% (costo de crecimiento)
            self.energy = 0.5


    def lower_if_low_energy(self):
        """
        Baja de nivel si energía < 25%.
        Al bajar, recupera energía al 100% para evitar efecto cascada.
        """
        if self.energy < 0.25 and self.size_level > 1 and not self.recently_downgraded:
            self.size_level -= 1
            self.size = self.size_level * self.size_step
            self.update_stats()

            # Recuperar energía al 100% al bajar nivel
            self.energy = 1.0

            self.recently_downgraded = True

        # Resetea la bandera cuando recupera energía > 50%
        if self.energy > 0.5:
            self.recently_downgraded = False


    # -------------------
    # Actualización de stats
    # -------------------
    def update_stats(self):
        """Penalización por nivel y ajuste de visión."""
        # Velocidad base penalizada
        self.speed = self.base_speed * (1 - 0.1 * (self.size_level - 1))

        # Visión aumenta con nivel (10% por nivel extra)
        self.vision = self.base_vision * (1 + 0.1 * (self.size_level - 1))

        # Reaplicar mutaciones (afectan velocidad, visión y consumo)
        self.apply_mutations()

    # -------------------
    # Mutaciones
    # -------------------
    def apply_mutations(self):
        """Ajusta stats y color según mutaciones activas."""
        # Reset stats base de velocidad y visión
        self.speed = self.base_speed * (1 - 0.1 * (self.size_level - 1))
        self.vision = self.base_vision * (1 + 0.1 * (self.size_level - 1))
        energy_factor = 1.0

        # Mutación roja: +20% speed, +20% consumo
        if 'red' in self.mutations:
            self.speed *= 1.2
            energy_factor *= 1.2

        # Mutación azul: +30% visión, -10% velocidad
        if 'blue' in self.mutations:
            self.vision *= 1.3
            self.speed *= 0.9

        # Mutación verde: -20% consumo, -10% velocidad
        if 'green' in self.mutations:
            energy_factor *= 0.8
            self.speed *= 0.9

        self.energy_cost_factor = energy_factor

        # Color combinado por mutaciones
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
        """
        Genera un nuevo organismo hijo con posibles mutaciones heredadas.
        """
        new_mutations = set(self.mutations)

        # Probabilidad de mutación nueva
        if random.random() < mutation_chance:
            possible = ['red', 'blue', 'green']
            available = [m for m in possible if m not in new_mutations]
            if available:
                new_mutations.add(random.choice(available))

        # Posición cercana al progenitor
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)

        return self.__class__(self.x + offset_x, self.y + offset_y, self.mix_colors(), mutations=new_mutations)

