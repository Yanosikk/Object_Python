import pygame
import sys
import random
import math


pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        angle = random.uniform(0, 2 * math.pi)
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx *= -1
            self.dy *= 0.95  
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy *= -1
            self.dx *= 0.95  

initial_speed = 2  

def check_collisions(balls):
    for i, ball in enumerate(balls):
        for other_ball in balls[i+1:]:
            dx = other_ball.x - ball.x
            dy = other_ball.y - ball.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= ball.radius + other_ball.radius:
                
                total_radius = ball.radius + other_ball.radius
                overlap = total_radius - distance
                overlap_normalized = (overlap / 2) / distance

                dx *= overlap_normalized
                dy *= overlap_normalized

                ball.x -= dx
                ball.y -= dy

                other_ball.x += dx
                other_ball.y += dy

                
                angle = math.atan2(dy, dx)
                angle += math.pi  
                angle %= 2 * math.pi

                norm = math.sqrt(ball.dx ** 2 + ball.dy ** 2)
                ball.dx = initial_speed * math.cos(angle)
                ball.dy = initial_speed * math.sin(angle)

                norm = math.sqrt(other_ball.dx ** 2 + other_ball.dy ** 2)
                other_ball.dx = initial_speed * math.cos(angle + math.pi)
                other_ball.dy = initial_speed * math.sin(angle + math.pi)

def main():
    clock = pygame.time.Clock()
    fps = 60


    num_balls = 10
    balls = [Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2) for _ in range(num_balls)]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
                                
                                
        screen.fill(BLACK)
        
        for ball in balls:
            ball.move()
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)

        check_collisions(balls)

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
