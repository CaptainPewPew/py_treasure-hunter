'''Author: Lei Yu
   Last Date Edited: 2021/05/11
   Purpose: a treasure hunter game,displays hall of fame then asks for size of
            game board, gives player 10 guesses to find 3 treasures that are
            randomly placed on the game board.

* diaply board
* board is made out of blocks
* hide treasure within the blocks
* player block moves through the blocks
* player is then able to search the block selected
* if no treasure game will check if there's treasures around
    * if there is threasure around it will show !
    * if there is no treasure around it will show ?
    * if treasure is found 'T' will show
* When all treasre is found it the game will end
* only ten moves allowed
* if player wins then score will be added to database (time and moves)
* a menu bar that allows the player to select game and scoreboard



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
block_size = 40;
grid_size = 10;

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.FPS = pygame.time.Clock()
        self.size = self.width, self.height = 640, 400
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()


    def cnc(self, row, col):
        return (row*(grid_size) + (col))

    def ncc(self, num):
        '''
            Return the coordinate using block number
        '''
        row = math.floor(num/(grid_size))
        col = num%(grid_size)
        return  row, col

    def init_board(self):
        for col in range(grid_size):
            for row in range(grid_size):
                self.block = Block(WHITE, row, col,self.font)
                self.block.rect.x = row*block_size
                self.block.rect.y = col*block_size

                self.block_list.add(self.block)
                self.all_sprites_list.add(self.block)

    def hide_treasures(self):
        self.target = random.sample(self.blocks,20)
        for i in self.target:
            i.hide_treasure()

    def check_block(self):
        self.collided = pygame.sprite.spritecollide(self.player, self.block_list, False)

        for b in self.collided:
            b.check()


    def on_init(self):
        pygame.init()

        #initializing window
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE| pygame.DOUBLEBUF)
        self._display_surf.fill(WHITE)
        pygame.display.set_caption("Treasure Hunt")

        self.font = pygame.font.SysFont("Comicsansms", 36)

        #initializing game board
        self.init_board()
        self.blocks = self.block_list.sprites()

        self.player = Player()
        self.player.rect.x = 0*block_size
        self.player.rect.y = 0*block_size
        self.all_sprites_list.add(self.player)

        #initialize treasures
        self.hide_treasures()

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE :
                self._running = False
            elif event.key == K_h:
                self.player.move_left()
            elif event.key == K_l:
                self.player.move_right()
            elif event.key == K_j:
                self.player.move_down()
            elif event.key == K_k:
                self.player.move_up()
            elif event.key == K_SPACE:
                self.check_block()


    def on_loop(self):
        self.FPS.tick(24)

    def on_render(self):
        self.player.update()
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


class Block(pygame.sprite.Sprite):
    def __init__(self, color, row, col, font):
        super().__init__()
        self.row = row;
        self.col = col;
        self.image = pygame.Surface([block_size,block_size])
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, ((0,0),(block_size,block_size)), 1)
        self.rect = self.image.get_rect()
        self.treasure = False;
        self.player_on = False;
        self.treasure_text = font.render("T",1,(10,10,10));

    def hide_treasure(self):
        self.treasure = True;

    def check(self):
        if (self.treasure):
            self.image.blit(self.treasure_text, (block_size/3,block_size/4))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.row = 0;
        self.col = 0;
        self.image = pygame.Surface([block_size,block_size])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, BLUE, ((0,0),(block_size,block_size)), 3)
        self.rect = self.image.get_rect()

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


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
