#!/usr/bin/env python3

'''
Author: Lei Yu
Last Date Edited: 2021/05/27
'''

import random
import pygame
import math
from pygame.locals import *

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

class App:
    def __init__(self):
        '''
        Initializes game constants
        '''
        self._running = True
        self._display_surf = None
        self.FPS = pygame.time.Clock()
        self.size = self.width, self.height = 640, 400
        self.treasures = 20
        self.grid_size = 10
        self.game_state = 0
        # 0 - game start menu
        # 1 - main game loop
        # 2 - game won
        # 3 - game lost
        # 4 - leader board menu

        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.counter_list = pygame.sprite.Group()

    def on_init(self):
        '''
        Initializes the game
        '''
        pygame.init()
        self.init_window()
        self.init_textfont()
        # start game menu
        self.init_menu()
        self._running = True

        # self.init_game()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if (event.key == K_q or event.key == K_ESCAPE):
                self._running = False
            elif (self.game_state == 0):
                if (event.key == K_RETURN):
                    self.game_state = 1
                    self.selection1.kill()
                    self.init_game()
            elif (self.game_state == 1):
                if (event.key == K_h or event.key == K_LEFT):
                    self.player.move_left()
                elif (event.key == K_l or event.key == K_RIGHT):
                    self.player.move_right()
                elif (event.key == K_j or event.key == K_DOWN):
                    self.player.move_down()
                elif (event.key == K_k or event.key == K_UP):
                    self.player.move_up()
                elif event.key == K_SPACE:
                    self.check_block()
                    self.check_game_state()
            elif (self.game_state == 2):
                pass
            elif (self.game_state == 3):
                pass
            elif (self.game_state == 4):
                pass

    def on_loop(self):
        self.FPS.tick(24)
        # self.player.update()
        # self.moves_counter.update()
        # self.treasures_counter.update()

    def on_render(self):
        if (self.game_state == 0):
            self._display_surf.fill(BLUE)
        elif (self.game_state == 1):
            self._display_surf.fill(WHITE)
        elif (self.game_state == 2):
            pass
        elif (self.game_state == 3):
            pass
        elif (self.game_state == 4):
            pass

        self.all_sprites_list.draw(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def init_window(self):
        '''
        initializing_window, sets window title and window size
        '''
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE| pygame.DOUBLEBUF)
        pygame.display.set_caption("Treasure Hunt")

    def init_textfont(self):
        self.font = pygame.font.SysFont(None, 36)
        self.treasure_text = self.font.render("T",1,(10,10,10))
        self.nothing_text = self.font.render("X",1,(10,10,10))

    def init_menu(self):
        self._display_surf.fill(BLUE)
        self.selection1 = Selection(self.font, "Start Game", 300, 300)
        self.all_sprites_list.add(self.selection1)



    def init_game(self):
        #intialize text and font
        self._display_surf.fill(WHITE)

        self.moves_counter = Counter(self.font, "Moves left: ", 40, 400, 100)
        self.counter_list.add(self.moves_counter)
        self.all_sprites_list.add(self.moves_counter)

        self.treasures_counter = Counter(self.font,"Treasures left: ", 20, 400, 200)
        self.counter_list.add(self.treasures_counter)
        self.all_sprites_list.add(self.treasures_counter)

        #initializing game board
        self.init_board()

        # blocks sprite list
        self.blocks = self.block_list.sprites()

        # Initialize Player
        self.player = Player()
        self.all_sprites_list.add(self.player)

        #initialize treasures
        self.hide_treasures()


    def cnc(self, row, col):
        '''
            retirm block number given coordinate
        '''
        return (row*(self.grid_size) + (col))

    def ncc(self, num):
        '''
            Return the coordinate using block number
        '''
        row = math.floor(num/(self.grid_size))
        col = num%(self.grid_size)
        return  row, col

    def init_board(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.block = Block(WHITE, row, col)

                self.block_list.add(self.block)
                self.all_sprites_list.add(self.block)

    def hide_treasures(self):
        self.target = random.sample(self.blocks,self.treasures)
        for i in self.target:
            i.hide_treasure()

    def check_block(self):
        collided = pygame.sprite.spritecollide(self.player, self.block_list, False)
        # print(f'row: {collided[0].row}')
        # print(f'col: {collided[0].col}')

        if (not(collided[0].digged)):
            self.moves_counter.set_count()
            # print(self.moves_counter.get_count())
            if (collided[0].dig()):
                self.draw_on_block(collided[0], self.treasure_text)
                self.treasures_counter.set_count()
            else:
                self.check_surrounding(collided[0])
                if (self.treasures_detected):
                    self.closeby_text = self.font.render(f'{self.treasures_detected}',1,(10,10,10))
                    self.draw_on_block(collided[0], self.closeby_text)
                    collided[0].digged = True
                else:
                    self.draw_on_block(collided[0], self.nothing_text)
                    collided[0].digged = True
        else:
            pass

    def draw_on_block(self, block, text):
        block.image.blit(text, (block.block_size/3,block.block_size/4))

    def check_surrounding(self, block):
        '''
            Return the number of treasures around block
        '''
        row, col = block.row, block.col
        self.treasures_detected = 0
        for i in (self.cnc(row-1,col-1), self.cnc(row-1,col), self.cnc(row-1,col+1), self.cnc(row,col-1), self.cnc(row,col+1), self.cnc(row+1,col-1), self.cnc(row+1,col), self.cnc(row+1,col+1)):
            try:
                if (self.blocks[i].treasure and i >= 0):
                    self.treasures_detected += 1
            except IndexError:
                continue

    def check_game_state(self):
        if (self.moves_counter.count <= 0):
            print("game lost")
        if (self.treasures_counter.count <= 0):
            print("game won")


class Block(pygame.sprite.Sprite):
    def __init__(self, color, row, col):
        super().__init__()
        self.row, self.col = row, col;
        self.block_size = 40;
        self.treasure = False
        self.player_on = False
        self.digged = False

        self.image = pygame.Surface([self.block_size,self.block_size])
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, ((0,0),(self.block_size,self.block_size)), 1)
        self.rect = self.image.get_rect()

        self.position_block(row,col)

    def position_block(self, row, col):
        self.rect.y = row*self.block_size
        self.rect.x = col*self.block_size

    def hide_treasure(self):
        self.treasure = True

    def dig(self):
        if (self.treasure):
            # self.treasure = False
            self.digged = True
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.row = 0;
        self.col = 0;
        self.block_size = 40;
        self.image = pygame.Surface([self.block_size,self.block_size])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, BLUE, ((0,0),(self.block_size,self.block_size)), 3)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move_right(self):
        self.col += 1
        if self.col > 9:
            self.col = 9

    def move_left(self):
        self.col -= 1
        if self.col < 0:
            self.col = 0

    def move_up(self):
        self.row -= 1
        if self.row < 0:
            self.row = 0

    def move_down(self):
        self.row += 1
        if self.row > 9:
            self.row = 9

    def update(self):
        self.rect.x = self.col * 40;
        self.rect.y = self.row * 40;

class Counter(pygame.sprite.Sprite):
    def __init__(self, font, text, count, x, y):
        super().__init__()
        self.message = text
        self.count = count
        self.font = font
        self.image = self.font.render(self.message + str(self.count),1,BLACK)
        self.rect = self.image.get_rect()

        self.place_counter(x,y)

    def place_counter(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_count(self):
        return self.count

    def set_count(self, num=-1):
        '''
        Will set the count of the counter, if count is not defined will automatically -1
        (Maybe just change it to -1, but this gives more funcationality)
        '''
        if (num == -1):
            self.count -= 1
        else:
            self.count = num

    def update(self):
        self.image = self.font.render(self.message + str(self.count),1,BLACK)

class Selection(pygame.sprite.Sprite):
    def __init__(self, font, text, x, y):
        super().__init__()
        self.message = text
        self.font = font
        self.image = self.font.render(self.message, 1, BLACK)
        self.rect = self.image.get_rect()
        self.place_selection(x,y)

    def place_selection(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def selected(self):
        pass

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
