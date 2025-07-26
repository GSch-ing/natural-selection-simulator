import pygame
import random
import math
from prey import Prey
from predator import Predator
from food import Food

import csv
import matplotlib.pyplot as plt


save_every = 100  # cada cuántos ticks guardar y graficar
tick_count = 0

########## --- Configuración inicial ---------------
WIDTH, HEIGHT = 1200, 700
BG_COLOR = (30, 30, 30)
FPS = 60

# Cantidades iniciales
INITIAL_PREY = 35
INITIAL_PREDATORS = 10
INITIAL_FOOD = 30

# Comida dinámica
BASE_MAX_FOOD = 30      # máximo base de comida
FOOD_RESPAWN_RATE = 1   # cuánta comida se genera por ciclo

def spawn_food(foods, max_food):
    """Repone comida solo hasta el máximo dinámico."""
    current_food = len(foods)
    if current_food < max_food:
        to_spawn = min(FOOD_RESPAWN_RATE, max_food - current_food)
        for _ in range(to_spawn):
            foods.append(Food(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Selección Natural")
    clock = pygame.time.Clock()

    # Para almacenar datos históricos
    history_prey = []
    history_predators = []
    history_food = []
    history_ticks = []
    save_every = 100  # cada cuántos ticks guardar y graficar
    tick_count = 0  # <-- definí esta variable acá

    # --- Listas iniciales ---
    preys = [Prey(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30), (200, 200, 200)) for _ in range(INITIAL_PREY)]
    predators = [Predator(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30)) for _ in range(INITIAL_PREDATORS)]
    foods = [Food(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30)) for _ in range(INITIAL_FOOD)]

    running = True
    while running:
        tick_count += 1  # Incrementar aquí dentro del loop
        clock.tick(FPS)

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Ajuste dinámico de comida máxima ---
        # Menos comida si hay muchas presas, un poco más si hay depredadores
        dynamic_max_food = BASE_MAX_FOOD - int(len(preys) * 0.5) + int(len(predators) * 0.3)
        dynamic_max_food = max(5, min(40, dynamic_max_food))  # clamp 5-40

        # --- Movimiento presas ---
        for prey in preys[:]:
            prey.move_towards_food(foods, predators, WIDTH, HEIGHT)

            # Comer comida
            for food in foods[:]:
                if math.hypot(prey.x - food.x, prey.y - food.y) < prey.size:
                    foods.remove(food)
                    prey.energy += 0.15  # menos energía por comida
                    prey.energy = min(1.0, prey.energy)
                    prey.food_counter -= 1

            # Reproducción (más exigente)
            if prey.food_counter <= 0:
                preys.append(prey.reproduce())
                prey.food_counter = 4

            # Muerte por inanición
            if prey.energy <= 0:
                preys.remove(prey)

        # --- Movimiento depredadores ---
        for predator in predators[:]:
            predator.move_towards_prey(preys, WIDTH, HEIGHT)

            # Cazar presa
            for prey in preys[:]:
                if math.hypot(predator.x - prey.x, predator.y - prey.y) < predator.size:
                    preys.remove(prey)
                    predator.energy += 0.8  # Más energía al cazar
                    predator.energy = min(1.0, predator.energy)
                    predator.food_counter -= 1

            # Reproducción dinámica: sólo si hay suficientes presas
            if predator.food_counter <= 0:
                child = predator.reproduce(len(preys))
                if child:
                    predators.append(child)
                predator.food_counter = 4

            # Muerte por inanición
            if predator.energy <= 0:
                predators.remove(predator)

        # --- Reposición de comida adaptativa ---
        spawn_food(foods, dynamic_max_food)

        # --- Dibujar ---
        screen.fill(BG_COLOR)
        for food in foods:
            food.draw(screen)
        for prey in preys:
            prey.draw(screen)
        for predator in predators:
            predator.draw(screen)

        # Contadores de debug
        font = pygame.font.SysFont(None, 24)
        text = font.render(
            f"Presas: {len(preys)} | Depredadores: {len(predators)} | Comida: {len(foods)} | MaxFood: {dynamic_max_food}",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (10, 10))

        pygame.display.flip()

        ##################

        # Guardar datos
        history_prey.append(len(preys))
        history_predators.append(len(predators))
        history_food.append(len(foods))
        history_ticks.append(tick_count)

        # Cada `save_every` ticks guardar CSV y generar gráfico
        if tick_count % save_every == 0:
            # Guardar CSV
            with open('sim_history.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Tick', 'Prey', 'Predators', 'Food'])
                for t, p, pr, f in zip(history_ticks, history_prey, history_predators, history_food):
                    writer.writerow([t, p, pr, f])

            # Graficar
            plt.figure(figsize=(10, 5))
            plt.plot(history_ticks, history_prey, label='Presas')
            plt.plot(history_ticks, history_predators, label='Depredadores')
            plt.plot(history_ticks, history_food, label='Comida')
            plt.xlabel('Ticks')
            plt.ylabel('Cantidad')
            plt.title('Evolución de la Simulación')
            plt.legend()
            plt.grid(True)
            plt.savefig('sim_history.png')
            plt.close()
        ###########


    pygame.quit()


if __name__ == "__main__":
    main()








