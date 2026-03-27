import pygame
import sys
from time import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot
from logger import log_state, log_event
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, BLACK



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0

    player_score = 0

    pygame.font.init()  
    font = pygame.font.SysFont("monospace", 35)

    def update_score_display(player_score):
        # The arguments are: text, antialias (True/False), color
        score_text = font.render(f"Score {player_score}", True, WHITE)
        return score_text

    score_surface = update_score_display(player_score)

    def gameover_score_display(player_score):
        # The arguments are: text, antialias (True/False), color
        line1 = font.render(f"Game over. Score {player_score}", True, WHITE)
        line2 = font.render("Press Q to exit", True, WHITE)
        text_height = font.get_height()
        total_height = text_height * 2
        score_surface = pygame.Surface((max(line1.get_width(), line2.get_width()), total_height))
        score_surface.fill(BLACK)  # Фон для текста
        score_surface.blit(line1, (0, 0))
        score_surface.blit(line2, (0, text_height))
        return score_surface


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    scores = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable) 
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable) 
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (shots, updatable, drawable) 

    paused = False

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over")
                screen.fill(BLACK)
                score_surface = gameover_score_display(player_score)
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(score_surface, score_rect)
                pygame.display.flip()
                paused = True

                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                            log_event("Game over. Waiting for quite")
                            sys.exit()
            
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    log_event("score + 1")
                    player_score += 1
                    score_surface = update_score_display(player_score)



        screen.fill("black")

        screen.blit(score_surface, (10, 10))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
