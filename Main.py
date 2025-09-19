import pygame
from pygame import Vector2

import Settings
from Apple import APPLE
from Snake import SNAKE

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = APPLE()
        self.running = True

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.apple.draw_apple(screen)
        self.snake.draw_snake(screen)

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.grow()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < Settings.CELL_NUMBER:
            self.game_over()
        if not 0 <= self.snake.body[0].y < Settings.CELL_NUMBER:
            self.game_over()
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()

    def game_over(self):
        print("GAME OVER")
        self.running = False

pygame.init()
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption(Settings.SCREEN_TITLE)
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while main_game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)

    #draw elements
    screen.fill(Settings.BLACK)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)