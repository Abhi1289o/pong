import pygame
import random
from enum import Enum

pygame.init()
font = pygame.font.SysFont('arial.ttf', 25)

class Constants:
    DISPLAY_WIDTH = 500
    DISPLAY_HEIGHT = 500
    RECT_LEN = 100
    RECT_WIDTH = 20
    CIRCLE_RADIUS = 10
    RECT_MOVE = 15
    BALL_X_MOVE = 5
    BALL_Y_MOVE = 3
    WHITE = (255, 255, 255)
    BALCK = (0, 0, 0)

class PongGame:
    def __init__(self):
        self.w = Constants.DISPLAY_WIDTH
        self.h = Constants.DISPLAY_HEIGHT
        self.center = [Constants.DISPLAY_WIDTH//2, Constants.DISPLAY_HEIGHT//2]
        self.rl = Constants.RECT_LEN
        self.rw = Constants.RECT_WIDTH
        self.xpos1 = 0
        self.ypos1 = Constants.DISPLAY_HEIGHT//2 - Constants.RECT_LEN//2
        self.xpos2 = Constants.DISPLAY_WIDTH - Constants.RECT_WIDTH
        self.ypos2 = Constants.DISPLAY_HEIGHT//2 - Constants.RECT_LEN//2
        self.xdir = random.choice([-1, 1])  # Random start direction
        self.ydir = random.choice([-1, 1])  # Random vertical movement
        self.display = pygame.display.set_mode((self.h, self.w))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        self.score = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.ypos1 > 0:
            self.ypos1 -= Constants.RECT_MOVE
        if keys[pygame.K_s] and self.ypos1 < self.h - self.rl:
            self.ypos1 += Constants.RECT_MOVE
        if keys[pygame.K_UP] and self.ypos2 > 0:
            self.ypos2 -= Constants.RECT_MOVE
        if keys[pygame.K_DOWN] and self.ypos2 < self.h - self.rl:
            self.ypos2 += Constants.RECT_MOVE

        # Ball movement
        self.center[0] += self.xdir * Constants.BALL_X_MOVE
        self.center[1] += self.ydir * Constants.BALL_Y_MOVE

        # Collision with paddles
        if self.center[0] <= self.xpos1 + self.rw + Constants.CIRCLE_RADIUS and self.ypos1 <= self.center[1] <= self.ypos1 + self.rl:
            self.score += 1
            self.xdir *= -1
            self.ydir = ((self.center[1] - (self.ypos1 + self.rl // 2)) / 10)  # Adjust bounce angle

        if self.center[0] +Constants.CIRCLE_RADIUS >= self.xpos2 and self.ypos2 <= self.center[1] <= self.ypos2 + self.rl:
            self.xdir *= -1
            self.score += 1
            self.ydir = ((self.center[1] - (self.ypos2 + self.rl // 2)) / 10)

        # Collision with top and bottom walls
        if self.center[1] <= Constants.CIRCLE_RADIUS or self.center[1] + Constants.CIRCLE_RADIUS >= self.h:
            self.ydir *= -1

        # Check if ball goes out of bounds (game over)
        if self.center[0] < self.xpos1 + self.rw or self.center[0] > self.xpos2:
            return True, self.score

        self.clock.tick(30)
        self.draw()
        return False, self.score

    def draw(self):
        self.display.fill(Constants.BALCK)
        pygame.draw.rect(self.display, Constants.WHITE, pygame.Rect(self.xpos1, self.ypos1, self.rw, self.rl))
        pygame.draw.rect(self.display, Constants.WHITE, pygame.Rect(self.xpos2, self.ypos2, self.rw, self.rl))
        pygame.draw.circle(self.display, Constants.WHITE, tuple(self.center), Constants.CIRCLE_RADIUS, 0)
        text = font.render("Score: " + str(self.score), True, Constants.WHITE)
        self.display.blit(text, [200, 0])
        pygame.display.update()

if __name__ == "__main__":
    game = PongGame()

    while True:
        gameover, score = game.move()

        if gameover:
            break

    print("Final Score:", score)
    pygame.quit()
    exit()
