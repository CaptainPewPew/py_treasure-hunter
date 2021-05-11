'''Author: Lei Yu
   Last Date Edited: 2021/05/11
   Purpose: a treasure hunter game,displays hall of fame then asks for size of
            game board, gives player 10 guesses to find 3 treasures that are
            randomly placed on the game board.
'''
import random
import pygame
from pygame.locals import *

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.FPS = pygame.time.Clock()
        self.size = self.width, self.height = 640, 400


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE| pygame.DOUBLEBUF)
        self._display_surf.fill(WHITE)
        pygame.display.set_caption("Treasure Hunt")

        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.block = Block(BLACK, 20, 20)
        self.block.rect.x = random.randrange(self.width)
        self.block.rect.y = random.randrange(self.height)

        self.block_list.add(self.block)
        self.all_sprites_list.add(self.block)


        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            print("I run")
        elif event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE :
                self._running = False

    def on_loop(self):
        #self.pressed_keys = pygame.key.get_pressed()
        #if self.pressed_keys[K_q]:
        #    event.type = pygame.QUIT

        self.FPS.tick(24)

    def on_render(self):
        #pygame.draw.line(self._display_surf, BLUE, (150,130), (130,170))
        #pygame.draw.line(self._display_surf, BLUE, (150,130), (170,170))
        #pygame.draw.line(self._display_surf, GREEN, (130,170), (170,170))
        #pygame.draw.circle(self._display_surf, BLACK, (100,50), (30))

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
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()



def main():
    print("WELCOME TO TREASURE HUNT!\n")
    #display_hall_of_fame()

    board = []

    make_board(board)
    hide_treasure(board)

    treasures_found = 0
    #gives 10 turn to player and displays game status information
    for guess in range(10,0,-1):
        if treasures_found == 3:
            break
        else :
            print("\nYou have %d guess left and have found %d/3 treasures.\n" %\
                  (guess,treasures_found))
            display_board(board)
            if make_user_move(board):
                treasures_found += 1

    #displays 'T' location
    display_board(board,True)
    #if player has won, player name is recorded in 'Winners.txt'
    if treasures_found == 3:
        print("CONGRATULATIONS!  You found ALL of the hidden treasure.\n")
        record_winner()
    else :
        print("OH NO! You only found %d/3 treasures.\n" %(treasures_found))
    print("\n*** GAME OVER ***")

def display_hall_of_fame():
    '''displays halls of fame shows empty if Winners.txt not found or empty'''
    try :
        hall_of_fame = open('Winners.txt', 'r')
        print(" Hall OF Fame ")
        print("==============")
        for line in hall_of_fame:
            print(line.strip().center(14))
        print("==============\n")
        hall_of_fame.close()
    except IOError:
        print(" Hall OF Fame ")
        print("==============")
        print("<-- Empty! -->")
        print("==============\n")

def record_winner():
    winner_name = input("What's your name stranger? ")
    hall_of_fame = open("Winners.txt",'a')
    hall_of_fame.write(str(winner_name) + "\n")
    hall_of_fame.close()

def make_board(board):
    ''' asks user for size of board and makes one'''
    sublist = []
    while True:
        try :
            row = int(eval(input("How many rows would you like (3-10): ")))
            column = int(eval(input("How many columns would you like (3-10): ")))
        except (NameError,SyntaxError,TypeError) :
            print("\nInteger values only! Please try again.\n")
            continue

        if column >= 3 and column <= 10 and row >= 3 and row <= 10:
            break
        else :
            print("\nInvalid board size!! Please try again.\n")

    #modifies board with the amount of column and rows suggested by user
    for cols in range(column):
        sublist.extend(' ')
    for rows in range(row):
        board.append(sublist[:])

def hide_treasure(board):
    '''puts three random treasure 'T' on the board with unique index, modifies
    board, but does not return any value'''
    treasure_hid = 0
    while treasure_hid != 3:
        row = random.randrange(len(board))
        column = random.randrange(len(board[0]))
        if board[row][column] != 'T':
            board[row][column] = 'T'
            treasure_hid += 1

def display_board(board,show_treasure = False):
    '''displays game board, if show_treasure = True, 'T' are displayed, and vise
    versa, does not return any value'''
    #prints column #s
    print(' ', end=' ')
    for _ in range(len(board[0])):
            if _ == (len(board[0])-1):
                    print(" %d " %(_))
                    break
            print(" %d " %(_), end=' ')
    #prints row #s and game board
    for row in range(len(board)):
            print(str(row)+":", end=' ')
            if show_treasure:
                print(' | '.join(board[row]))
            else :
                print(' | '.join(board[row]).replace('T',' '))
            print('  ' + '+'.join(['---']*len(board[0])))
    print()

def radar(board,row,column):
    for row_set in [-1,0,1]:
        for col_set in [-1,0,1]:
            try :
                if board[row+(row_set)][column+(col_set)] == 'T':
                    return True
            except IndexError:
                pass

def make_user_move(board):
    '''asks user for column & row, exception handles if input are interger and
    input validates if values between 0 and 4. Returns true(places '$') if
    found treasure, return False if treasure not found.(places '!' if treasure
    is close within 1 block, and 'X' otherwise'''
    move = True
    while move:
        try :
            row = eval(input("What row would you like to search (0-%d): " %(len(board)-1)))
            column = eval(input("What col would you like to search (0-%d): " %(len(board[0])-1)))
            if row <= (len(board)-1) and row >= 0 and column <= (len(board[0])-1) and column >= 0:
            #checks if board index has been checked
                if board[row][column] == ' ' or board[row][column] == 'T':
                    move = False
                else :
                    print("\nYou already tried there, please pick again.\n")
            else :
                print("\nSorry, invalid location. Please try again!\n")
        except (NameError,SyntaxError,TypeError,ValueError):
            print("\nIntegers only for row and column values. Please try again!\n")
            continue

    if board[row][column] == 'T':
        print("\nYES!  You found a treasure.\n")
        board[row][column] = "$"
        return True
    else :
        if radar(board,row,column):
            print("\nVery close, treasure is near...\n")
            board[row][column] = "!"
        else:
            print("\nNothing there.")
            board[row][column] = "X"
        return False

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
