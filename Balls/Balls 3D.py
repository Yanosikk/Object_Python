import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Bouncing Balls 3D")

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

initial_speed = 2

class Ball:
    def __init__(self, x, y, z, radius, speed):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        )
        self.speed = speed
        angle_xy = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(0, 2 * math.pi)
        self.dx = self.speed * math.cos(angle_xy)
        self.dy = self.speed * math.sin(angle_xy)
        self.dz = self.speed * math.sin(angle_z)

    def move(self, slowdown_factor=1.0):
        self.x += self.dx * slowdown_factor
        self.y += self.dy * slowdown_factor
        self.z += self.dz * slowdown_factor

        if self.x - self.radius <= -WIDTH / 2 or self.x + self.radius >= WIDTH / 2:
            self.dx *= -1
        if self.y - self.radius <= -HEIGHT / 2 or self.y + self.radius >= HEIGHT / 2:
            self.dy *= -1
        if self.z - self.radius <= -200 or self.z + self.radius >= 200:
            self.dz *= -1

def draw_ball(ball):
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_position = (50, 50, 50, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glPushMatrix()
    glTranslatef(ball.x, ball.y, ball.z)
    draw_colored_sphere(ball.radius, 32, 32, ball.color)
    glPopMatrix()

def draw_colored_sphere(radius, slices, stacks, color):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, color)
    
    gluSphere(quad, radius, slices, stacks)

def check_collisions(balls):
    for i, ball in enumerate(balls):
        for other_ball in balls[i + 1:]:
            dx = other_ball.x - ball.x
            dy = other_ball.y - ball.y
            dz = other_ball.z - ball.z
            distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            if distance <= ball.radius + other_ball.radius:
                total_radius = ball.radius + other_ball.radius
                overlap = total_radius - distance
                overlap_normalized = (overlap / 2) / distance

                dx *= overlap_normalized
                dy *= overlap_normalized
                dz *= overlap_normalized

                ball.x -= dx
                ball.y -= dy
                ball.z -= dz

                other_ball.x += dx
                other_ball.y += dy
                other_ball.z += dz

                angle_xy = math.atan2(dy, dx)
                angle_xy += math.pi
                angle_xy %= 2 * math.pi

                angle_z = math.asin(dz / distance)
                angle_z += math.pi
                angle_z %= 2 * math.pi

                norm = math.sqrt(ball.dx ** 2 + ball.dy ** 2)
                ball.dx = initial_speed * math.cos(angle_xy)
                ball.dy = initial_speed * math.sin(angle_xy)
                ball.dz = initial_speed * math.sin(angle_z)

                norm = math.sqrt(other_ball.dx ** 2 + other_ball.dy ** 2)
                other_ball.dx = initial_speed * math.cos(angle_xy + math.pi)
                other_ball.dy = initial_speed * math.sin(angle_xy + math.pi)
                other_ball.dz = initial_speed * math.sin(angle_z + math.pi)

def main():
    clock = pygame.time.Clock()
    fps = 60

    num_balls = 30
    balls = [
    Ball(
        random.uniform(-WIDTH / 2 + 50, WIDTH / 2 - 50),
        random.uniform(-HEIGHT / 2 + 50, HEIGHT / 2 - 50),
        random.uniform(-200, 200),
        20,
        2,
    )
    for _ in range(num_balls)
]

    slowdown_factor = 1.0
    font = pygame.font.Font(None, 36)

    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 500.0)
    glTranslatef(0.0, 0.0, -250)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if slowdown_factor == 1.0:
                        slowdown_factor = 0.5
                    else:
                        slowdown_factor = 1.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)

        
        for ball in balls:
            ball.move(slowdown_factor)
            draw_ball(ball)

        check_collisions(balls)

        pygame.display.flip()
        pygame.time.wait(10)
        clock.tick(fps)

if __name__ == "__main__":
    main()
