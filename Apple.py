import pygame
from pygame import Vector2
from random import randint
from Settings import CELL_SIZE, CELL_NUMBER, SCOREBOARD_HEIGHT


class APPLE:
    def __init__(self):
        # create an x and y
        self.x = randint(0, CELL_NUMBER-1)
        self.y = randint(SCOREBOARD_HEIGHT//CELL_SIZE, CELL_NUMBER+ SCOREBOARD_HEIGHT//CELL_SIZE - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load('assets/Graphics/apple.png').convert_alpha()

    # draw a square
    def draw_apple(self,screen):
        #create a rect
        x_pos = self.pos.x * CELL_SIZE
        y_pos = self.pos.y * CELL_SIZE
        apple_rect = pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
        #draw a rect
        #pygame.draw.rect(screen,RED,apple_rect)
        screen.blit(self.apple, apple_rect)

    def randomize(self):
        self.x = randint(0, CELL_NUMBER-1)
        self.y = randint(SCOREBOARD_HEIGHT//CELL_SIZE, CELL_NUMBER + SCOREBOARD_HEIGHT//CELL_SIZE - 1)
        self.pos = Vector2(self.x, self.y)
