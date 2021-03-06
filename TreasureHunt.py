#!/usr/bin/env python3

'''
Author: Lei Yu
Last Date Edited: 2021/05/27


implement adding name when player wins
'''

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
import random
import pygame
import math
import sql
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
        self.connection = sql.create_connection("leader_board.db")
        sql.create_score_table(self.connection)
        self.game_state = 0
        # 0 - game start menu
        # 1 - main game loop
        # 2 - game won
        # 3 - leader board menu

        self.block_list = pygame.sprite.Group()
        self.text_list = pygame.sprite.Group()
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
                    if (self.selection1.selected):
                        self.game_state = 1
                        self.init_game()
                        self.selection1.kill()
                        self.selection2.kill()
                        self.selection3.kill()
                    elif (self.selection2.selected):
                        self.game_state = 3
                        self.show_leaderboard()
                        self.selection1.kill()
                        self.selection2.kill()
                        self.selection3.kill()
                    elif (self.selection3.selected):
                        self._running = False
                elif (event.key == K_1):
                    self.select_start()
                elif (event.key == K_2):
                    self.select_leader()
                elif (event.key == K_3):
                    self.select_quit()
                elif (event.key == K_k or event.key == K_UP):
                    self.menu_select("up")
                elif (event.key == K_j or event.key == K_DOWN):
                    self.menu_select("down")
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
                else :
                    print("Game is wrecked")
            elif (self.game_state == 2):
                pass
            elif (self.game_state == 3):
                pass

    def on_loop(self):
        self.FPS.tick(24)
        if (self.game_state == 1):
            self.player.update()
            self.moves_counter.update()
            self.treasures_counter.update()

    def on_render(self):
        if (self.game_state == 0):
            self._display_surf.fill(GREEN)
        elif (self.game_state == 1):
            self._display_surf.fill(WHITE)
        elif (self.game_state == 2 or self.game_state ==3):
            self._display_surf.fill(RED)

        self.all_sprites_list.draw(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        self.connection.close()
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
        self.selection1 = Selection(self.font, "Start Game", 200, 200)
        self.selection2 = Selection(self.font, "Leader Board", 200, 230)
        self.selection3 = Selection(self.font, "Quit", 200, 260)
        self.selections = (self.selection1, self.selection2, self.selection3)
        self.all_sprites_list.add(self.selection1)
        self.all_sprites_list.add(self.selection2)
        self.all_sprites_list.add(self.selection3)
        self.selection1.select()

    def select_start(self):
        self.selection1.select()
        self.selection2.deselect()
        self.selection3.deselect()

    def select_leader(self):
        self.selection1.deselect()
        self.selection2.select()
        self.selection3.deselect()

    def select_quit(self):
        self.selection1.deselect()
        self.selection2.deselect()
        self.selection3.select()

    def menu_select(self, direction):
        if (direction == "up"):
            if (self.selection2.selected == 1):
                self.select_start()
            elif (self.selection3.selected == 1):
                self.select_leader()
        elif (direction == "down"):
            if (self.selection1.selected == 1):
                self.select_leader()
            elif (self.selection2.selected ==1):
                self.select_quit()

    def init_game(self):
        #intialize text and font
        self._display_surf.fill(WHITE)

        self.moves_counter = Counter(self.font, "Moves made: ", 0, 400, 100)
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

    def show_leaderboard(self):
        '''
        0, name
        1, score
        2, date
        '''
        top_ten = sql.show_top_ten(self.connection)
        a = -1
        for i in top_ten:
            a += 1
            entry = Text(self.font, '{0:<10} {1:>5} {2:10}'.format(i[0], i[1], i[2]), 50, 50+(a*25))
            self.text_list.add(entry)
            self.all_sprites_list.add(entry)

        message_quit = Text(self.font, 'Press q to quit', 250, 350)
        self.text_list.add(message_quit)
        self.all_sprites_list.add(message_quit)

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
            self.moves_counter.set_count(1)
            # print(self.moves_counter.get_count())
            if (collided[0].dig()):
                self.draw_on_block(collided[0], self.treasure_text)
                self.treasures_counter.set_count(-1)
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
        current_cord = self.cnc(row, col)
        self.treasures_detected = 0
        check_list = (-11, -10, -9, -1, 1, 9, 10, 11 )
        # print(f'current cord = {current_cord}')
        # print(row, col)

        try:
            if (col == 0 and row == 0):
                for i in (1, 10, 11):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            elif (col == 0 and row == 9):
                for i in (1, -9, -10):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            elif (col == 0):
                for i in (-10, -9, 1, 10, 11):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            elif (col == 9 and row == 0): #top right corner
                for i in (-1, 9, 10):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            elif (col == 9 and row == 9):
                for i in (-11, -10, -1):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            elif (col == 9):
                for i in (-11, -10, -1, 9, 10):
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
            else:
                for i in check_list:
                    if (self.blocks[current_cord + i].treasure):
                        self.treasures_detected += 1
        except IndexError:
            pass

    def check_game_state(self):
        if (self.treasures_counter.count <= 0):
            self.store_score(self.moves_counter.count)
            for sprite in self.all_sprites_list.sprites():
                sprite.kill()
            self.game_state = 2
            self.show_leaderboard()
            print("game won")

    def store_score(self, score):
        name = "Lei"
        sql.add_entry(self.connection, name, score)


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

    def set_count(self, num):
        self.count += num

    def update(self):
        self.image = self.font.render(self.message + str(self.count),1,BLACK)

class Text(pygame.sprite.Sprite):
    def __init__(self,font, message, x, y):
        super().__init__()
        self.message = message
        self.font = font
        self.image = self.font.render(self.message,1,BLACK)
        self.rect = self.image.get_rect()
        self.place(x,y)

    def place(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Selection(pygame.sprite.Sprite):
    def __init__(self, font, text, x, y):
        super().__init__()
        self.message = text
        self.font = font
        self.image = self.font.render(self.message, 1, BLACK)
        self.rect = self.image.get_rect()
        self.place_selection(x,y)
        self.selected = 0

    def place_selection(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def select(self):
        self.selected = 1
        self.image = self.font.render(self.message, 1, WHITE)

    def deselect(self):
        self.selected = 0
        self.image = self.font.render(self.message, 1, BLACK)



if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
