import pygame
import random
from prey import Prey
from predator import Predator
from food import Food

WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
FPS = 60

MAX_FOOD = 40
FOOD_SPAWN_INTERVAL = 2000  # ms
MAX_PREYS = 50
MAX_PREDATORS = 20

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Crear presas iniciales
    preys = []
    for _ in range(6):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        preys.append(Prey(x, y, color))

    # Crear depredadores iniciales
    predators = []
    for _ in range(3):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        predators.append(Predator(x, y))

    # Crear comida inicial
    foods = [Food.spawn_random(WIDTH, HEIGHT) for _ in range(MAX_FOOD // 2)]

    # Temporizador para comida
    food_timer = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Spawn de comida controlado ---
        now = pygame.time.get_ticks()
        if now - food_timer > FOOD_SPAWN_INTERVAL and len(foods) < MAX_FOOD:
            for _ in range(2):
                if len(foods) < MAX_FOOD:
                    foods.append(Food.spawn_random(WIDTH, HEIGHT))
            food_timer = now

        # --- Actualizar presas ---
        for prey in preys[:]:
            prey.move_towards_food(foods, predators, WIDTH, HEIGHT)

            # Comer comida
            for food in foods:
                dist = ((prey.x - food.x)**2 + (prey.y - food.y)**2) ** 0.5
                if dist < prey.size + food.size:
                    prey.energy = min(1.0, prey.energy + 0.3)
                    prey.grow_if_ready()

                    prey.food_counter -= 1
                    if prey.food_counter <= 0 and len(preys) < MAX_PREYS:
                        child = prey.reproduce()
                        preys.append(child)
                        prey.food_counter = 8  # nuevo requisito

                    foods.remove(food)
                    break

            if prey.energy <= 0:
                preys.remove(prey)

        # --- Actualizar depredadores ---
        for predator in predators[:]:
            predator.move_towards_prey(preys, WIDTH, HEIGHT)

            # Cazar presas
            for prey in preys:
                dist = ((predator.x - prey.x)**2 + (predator.y - prey.y)**2) ** 0.5
                if dist < predator.size + prey.size and predator.size_level >= prey.size_level:
                    predator.energy = min(1.0, predator.energy + 0.25)  # menos energía que antes
                    predator.grow_if_ready()

                    predator.food_counter -= 1
                    if predator.food_counter <= 0 and len(predators) < MAX_PREDATORS:
                        predators.append(predator.reproduce())
                        predator.food_counter = 12  # nuevo requisito

                    preys.remove(prey)
                    break

            if predator.energy <= 0:
                predators.remove(predator)

        # --- Dibujar ---
        screen.fill(BG_COLOR)
        for food in foods:
            food.draw(screen)
        for prey in preys:
            prey.draw(screen)
        for predator in predators:
            predator.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()





