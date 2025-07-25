import pygame
import random
from organism import Organism
from food import Food

# Configuracion
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Crear varios organismos con colores y posiciones aleatorias
    organisms = []
    for _ in range(10): # cantidad de organismos inicial
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        organisms.append(Organism(x, y, color))
    
    # Crear comida inicial
    foods = []
    for _ in range(5):  # cantidad de comida inicial
        foods.append(Food.spawn_random(WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mover organismos
        for organism in organisms:
            organism.move(WIDTH, HEIGHT, foods)
        
        # Revisar colisiones con comida
        for organism in organisms:
            for food in foods:
                dist = ((organism.x - food.x)**2 + (organism.y - food.y)**2) ** 0.5
                if dist < organism.size + food.size:
                    organism.energy = min(1.0, organism.energy + 0.3)
                    foods.remove(food)
                    foods.append(Food.spawn_random(WIDTH, HEIGHT))
                    break

        # Eliminar organismos sin energía
        organisms = [o for o in organisms if o.energy > 0]
        

        # Dibujar area
        screen.fill(BG_COLOR)
        # Dibujar comida
        for food in foods:
            food.draw(screen)
        # Dibujar organismos
        for organism in organisms:
            organism.draw(screen, BG_COLOR, vision_radius=100)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
