import pygame
import random
import sys

from paddle import Paddle
from ball import Ball


class Pong:
    HEIGHT = 800
    WIDTH = 1600

    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 100

    BALL_WIDTH = 10
    BALL_VELOCITY = 10

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()

        # screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.central_line = pygame.Rect(self.WIDTH/2, 0, 1, self.HEIGHT)

        # creates the objects
        self.scores = [0,0]
        self.start_round()


    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.screen.fill(self.BLACK)

            self.check_ball_paddle()
            self.check_ball_out_board()

            self.move_paddles()
            self.move_ball()

            if(self.check_point()):
                self.start_round()

            self.draw_center_line()
            self.draw_paddles()
            self.draw_ball()




            pygame.display.flip()
            self.clock.tick(60)



    def create_paddles(self):
        self.paddles = []
        self.paddles.append(Paddle(self.BALL_VELOCITY,
            pygame.K_w,
            pygame.K_s,
            0,
            self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
            self.PADDLE_WIDTH,
            self.PADDLE_HEIGHT))

        self.paddles.append(Paddle(  # The right paddle
            self.BALL_VELOCITY,
            pygame.K_UP,
            pygame.K_DOWN,
            self.WIDTH - self.PADDLE_WIDTH,
            self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2,
            self.PADDLE_WIDTH,
            self.PADDLE_HEIGHT
        ))

    def draw_paddles(self):
        for paddle in self.paddles:
            pygame.draw.rect(self.screen, self.WHITE, paddle)

    def move_paddles(self):
        for paddle in self.paddles:
            paddle.move(self.HEIGHT)


    def draw_ball(self):
        for ball in self.balls:
            pygame.draw.rect(self.screen, self.WHITE, ball)

    def create_ball(self):
        self.balls = []
        self.balls.append(Ball(
            self.BALL_VELOCITY,
            self.WIDTH / 2 - self.BALL_WIDTH / 2,
            self.HEIGHT / 2 - self.BALL_WIDTH / 2,
            self.BALL_WIDTH,
            self.BALL_WIDTH
        ))
        

    def move_ball(self):
        for ball in self.balls:
            ball.move()

    def check_ball_paddle(self):
        for ball in self.balls:
            for paddle in self.paddles:
                if ball.colliderect(paddle):
                    ball.velocity = -ball.velocity
                    ball.angle = random.randint(-10, 10)
                    break

    def check_ball_out_board(self):
        for ball in self.balls:
            if ball.y > self.HEIGHT or ball.y < 0:
                ball.angle = - ball.angle

    def check_point(self):
        restart = False

        for ball in self.balls:
            if ball.x > self.WIDTH:
                self.scores[1] += 1
                restart = True

            if ball.x < 0:
                self.scores[0] += 1
                restart = True
        return restart

    def draw_center_line(self):
        pygame.draw.rect(self.screen, self.WHITE, self.central_line)


    def start_round(self):
        self.create_paddles()
        self.create_ball()


if __name__ == "__main__":
    pong = Pong()
    pong.game_loop()
