import pygame
from pygame import Vector2
import settings
from apple import APPLE
from snake import SNAKE
from resources import get_font

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

def draw_background():
    background_color = settings.BLACK
    screen.fill(background_color)
    for col in range(settings.CELL_NUMBER):
        for row in range(settings.CELL_NUMBER):
            if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                background_color = settings.GREEN
            elif (col % 2 == 1 and row % 2 == 0) or (col % 2 == 0 and row % 2 == 1):
                background_color = settings.LIGHTGREEN
            background_rect = pygame.Rect(col * settings.CELL_SIZE, row * settings.CELL_SIZE+settings.SCOREBOARD_HEIGHT,settings.CELL_SIZE,settings.CELL_SIZE)
            pygame.draw.rect(screen,background_color,background_rect)


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = APPLE()
        self.running = True
        self.high_score = load_high_score()
        self.score = 0
        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == SCREEN_UPDATE:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != Vector2(0, 1):
                        self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and self.snake.direction != Vector2(0, -1):
                        self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and self.snake.direction != Vector2(1, 0):
                        self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and self.snake.direction != Vector2(-1, 0):
                        self.snake.direction = Vector2(1, 0)

            # draw elements
            self.draw_elements()
            pygame.display.update()
            clock.tick(settings.CLOCK)

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
        if not 0 <= self.snake.body[0].x < settings.CELL_NUMBER:
            self.game_over()
        if not settings.SCOREBOARD_HEIGHT//settings.CELL_SIZE <= self.snake.body[0].y < settings.CELL_NUMBER + settings.SCOREBOARD_HEIGHT//settings.CELL_SIZE:
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
        score_surface = game_font.render(score_text, True, settings.WHITE)
        scoreboard_rect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCOREBOARD_HEIGHT)
        pygame.draw.rect(screen, settings.SCOREBOARD_COLOR, scoreboard_rect,0,10)
        pygame.draw.rect(screen, settings.WHITE, scoreboard_rect, 2,10)
        score_rect = score_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCOREBOARD_HEIGHT // 2))
        apple_rect_1 = self.apple.apple.get_rect(midright=(score_rect.left,score_rect.centery))
        apple_rect_2 = self.apple.apple.get_rect(midleft=(score_rect.right, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(self.apple.apple, apple_rect_1)
        screen.blit(self.apple.apple, apple_rect_2)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption(settings.SCREEN_TITLE)
game_font = get_font('PoetsenOne-Regular.ttf', 40)
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = GAME()