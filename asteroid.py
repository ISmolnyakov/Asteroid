import pygame, random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)


    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            new_angle = random.uniform(20,50)
            vector_one = self.velocity.rotate(new_angle)
            vector_two = self.velocity.rotate(new_angle*-1)
            new_radius = self.radius-ASTEROID_MIN_RADIUS
            new_asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_one.velocity = vector_one * 1.2
            new_asteroid_two.velocity = vector_two * 1.2