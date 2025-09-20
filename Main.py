import pygame
from pygame import Vector2

import Settings
from Apple import APPLE
from Snake import SNAKE


def draw_background():
    background_color = Settings.BLACK
    screen.fill(background_color)
    for col in range(Settings.CELL_NUMBER):
        for row in range(Settings.CELL_NUMBER):
            if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                background_color = Settings.GREEN
            elif (col % 2 == 1 and row % 2 == 0) or (col % 2 == 0 and row % 2 == 1):
                background_color = Settings.LIGHTGREEN
            background_rect = pygame.Rect(col * Settings.CELL_SIZE, row * Settings.CELL_SIZE+Settings.SCOREBOARD_HEIGHT,Settings.CELL_SIZE,Settings.CELL_SIZE)
            pygame.draw.rect(screen,background_color,background_rect)


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = APPLE()
        self.running = True
        self.high_score = load_high_score()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        draw_background()
        self.draw_score()
        self.apple.draw_apple(screen)
        self.snake.draw_snake(screen)

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.grow()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < Settings.CELL_NUMBER:
            self.game_over()
        if not Settings.SCOREBOARD_HEIGHT//Settings.CELL_SIZE <= self.snake.body[0].y < Settings.CELL_NUMBER + Settings.SCOREBOARD_HEIGHT//Settings.CELL_SIZE:
            self.game_over()
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()

    def game_over(self):
        print("GAME OVER")
        self.save_high_score()
        self.running = False

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def draw_score(self):
        self.score = len(self.snake.body)-3
        if self.score > self.high_score: self.high_score = self.score
        score_text = f"Score: {self.score}   High Score: {self.high_score}"
        score_surface = game_font.render(score_text, True, Settings.WHITE)
        scoreboard_rect = pygame.Rect(0, 0, Settings.SCREEN_WIDTH, Settings.SCOREBOARD_HEIGHT)
        pygame.draw.rect(screen, Settings.BLACK, scoreboard_rect,0,10)
        pygame.draw.rect(screen, Settings.WHITE, scoreboard_rect, 2,10)
        score_rect = score_surface.get_rect(center=(Settings.SCREEN_WIDTH // 2, Settings.SCOREBOARD_HEIGHT // 2))
        screen.blit(score_surface, score_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption(Settings.SCREEN_TITLE)
game_font = pygame.font.Font('assets/Font/PoetsenOne-Regular.ttf',40)
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
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)