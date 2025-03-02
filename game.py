import pygame
import random

pygame.init()
font = pygame.font.SysFont('arial.ttf', 25)

class PongGame:
    def __init__(self):
        self.w = 500
        self.h = 500
        self.center = [250, 250]
        self.rl = 100
        self.rw = 20
        self.xpos1 = 0
        self.ypos1 = 200
        self.xpos2 = 480
        self.ypos2 = 200
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
            self.ypos1 -= 15
        if keys[pygame.K_s] and self.ypos1 < self.h - self.rl:
            self.ypos1 += 15
        if keys[pygame.K_UP] and self.ypos2 > 0:
            self.ypos2 -= 15
        if keys[pygame.K_DOWN] and self.ypos2 < self.h - self.rl:
            self.ypos2 += 15

        # Ball movement
        self.center[0] += self.xdir * 5
        self.center[1] += self.ydir * 3

        # Collision with paddles
        if self.center[0] <= self.xpos1 + 30 and self.ypos1 <= self.center[1] <= self.ypos1 + self.rl:
            self.score += 1
            self.xdir *= -1
            self.ydir = ((self.center[1] - (self.ypos1 + self.rl // 2)) / 10)  # Adjust bounce angle

        if self.center[0] >= self.xpos2 - 10 and self.ypos2 <= self.center[1] <= self.ypos2 + self.rl:
            self.xdir *= -1
            self.score += 1
            self.ydir = ((self.center[1] - (self.ypos2 + self.rl // 2)) / 10)

        # Collision with top and bottom walls
        if self.center[1] <= 10 or self.center[1] >= self.h - 10:
            self.ydir *= -1

        # Check if ball goes out of bounds (game over)
        if self.center[0] < self.xpos1 + 20 or self.center[0] > self.xpos2:
            return True, self.score

        self.clock.tick(30)
        self.draw()
        return False, self.score

    def draw(self):
        self.display.fill((0, 0, 0))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(self.xpos1, self.ypos1, 20, 100))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(self.xpos2, self.ypos2, 20, 100))
        pygame.draw.circle(self.display, (255, 255, 255), tuple(self.center), 10, 0)
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
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
