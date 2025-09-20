import pygame
from pygame import Vector2
from Settings import CELL_SIZE,CELL_NUMBER,WHITE

class SNAKE:
    def __init__(self):
        self.body = [Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.direction = Vector2(1, 0)

        self.head_up = pygame.image.load('assets/Graphics/head_up.png')
        self.head_down = pygame.image.load('assets/Graphics/head_down.png')
        self.head_left = pygame.image.load('assets/Graphics/head_left.png')
        self.head_right = pygame.image.load('assets/Graphics/head_right.png')

        self.tail_up = pygame.image.load('assets/Graphics/tail_up.png')
        self.tail_down = pygame.image.load('assets/Graphics/tail_down.png')
        self.tail_left = pygame.image.load('assets/Graphics/tail_left.png')
        self.tail_right = pygame.image.load('assets/Graphics/tail_right.png')

        self.body_horizontal = pygame.image.load('assets/Graphics/body_horizontal.png')
        self.body_vertical = pygame.image.load('assets/Graphics/body_vertical.png')

        self.body_tr = pygame.image.load('assets/Graphics/body_tr.png')
        self.body_tl = pygame.image.load('assets/Graphics/body_tl.png')
        self.body_br = pygame.image.load('assets/Graphics/body_br.png')
        self.body_bl = pygame.image.load('assets/Graphics/body_bl.png')

        self.crunch_sound = pygame.mixer.Sound('assets/Sound/crunch.wav')

    def draw_snake(self,screen):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            #create a rect
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
            #what direction are we going
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == (len(self.body)-1):
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1, 0): self.head = self.head_left
        elif head_direction == Vector2(-1, 0): self.head = self.head_right
        elif head_direction == Vector2(0, 1): self.head = self.head_up
        elif head_direction == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_direction = self.body[len(self.body)-1] - self.body[len(self.body)-2]
        if tail_direction == Vector2(1, 0): self.tail = self.tail_right
        elif tail_direction == Vector2(-1, 0): self.tail = self.tail_left
        elif tail_direction == Vector2(0, 1): self.tail = self.tail_down
        elif tail_direction == Vector2(0, -1): self.tail = self.tail_up

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def grow(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def play_crunch_sound(self):
        self.crunch_sound.play()