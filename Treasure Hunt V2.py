'''Author: Lei Yu
   Last Date Edited: 2016/01/16
   Purpose: a 5x5 treasure hunter game, gives player 10 guesses to find 3 
            treasures randomly placed on the game board.
'''
import random

def main():
    print "WELCOME TO TREASURE HUNT!\n"
    
    treasures_found = 0
    board = [[' ', ' ', ' ',' ', ' '], [' ', ' ', ' ',' ', ' '], 
             [' ', ' ', ' ',' ', ' '], [' ', ' ', ' ',' ', ' '], 
             [' ', ' ', ' ',' ', ' ']]
    
    hide_treasure(board)
    
    #gives 10 turn to player and displays game status information
    for guess in range(10,0,-1):
        if treasures_found == 3:
            break
        else :
            print "You have %d guesses left and have found %d/3 treasures.\n" \
                  %(guess,treasures_found)
            display_board(board)
            if make_user_move(board):
                treasures_found += 1
                
    #displays 'T' location and end game results            
    display_board(board,True)    
    if treasures_found == 3:
        print "CONGRATULATIONS!  You found ALL of the hidden treasure.\n"  
    else :
        print "OH NO! You only found %d/3 treasures.\n" %(treasures_found)
    print "*** GAME OVER ***"

def hide_treasure(board):
    '''puts three random treasure 'T' on the board with unique index, modifies 
    board, this function does not return any value'''
    treasure_hid = 0
    while treasure_hid != 3:
        row = random.randrange(5)
        column = random.randrange(5)
        if board[row][column] != 'T':
            board[row][column] = 'T'
            treasure_hid += 1
            
def display_board(board,show_treasure = False):
    '''displays game board, if show_treasure = True 'T' are displayed, otherwise
    'T' is hidden, this function does not return any value'''
    mask = ' '
    if show_treasure:
        mask = 'T'
    print "   0   1   2   3   4"
    print "0: "+' | '.join(board[0]).replace('T',mask)
    print "  ---+---+---+---+---"
    print "1: "+' | '.join(board[1]).replace('T',mask)
    print "  ---+---+---+---+---"
    print "2: "+' | '.join(board[2]).replace('T',mask)
    print "  ---+---+---+---+---"
    print "3: "+' | '.join(board[3]).replace('T',mask)
    print "  ---+---+---+---+---"
    print "4: "+' | '.join(board[4]).replace('T',mask)
    print "  ---+---+---+---+---\n"

def radar(board,row,column):
    for row_set in [-1,0,1]:
        for col_set in [-1,0,1]:
            try :
                if board[row+(row_set)][column+(col_set)] == 'T':
                    return True
            except IndexError:
                pass
    
def make_user_move(board):
    '''takes in a list with sublist for treasure hunt, asks user for column & 
    row, exception handles if input are interger and input validates if values 
    are between 0 and 4. Returns true(places '$') if found treasure,otherwise if
    blocks around index is 'T' places '!' if not places 'X' and returns False''' 
    move = True
    while move:
        try :
            row = input("What row would you like to search (0-4): ")
            column = input("What col would you like to search (0-4): ")
            if row <= 4 and row >= 0 and column <= 4 and column >= 0:
                #checks if board index has been checked
                if board[row][column] == ' ' or board[row][column] == 'T':
                    move = False
                else :
                    print "\nYou already tried there, please pick again.\n"
            else :
                print "\nSorry, invalid location. Please try again!\n"
        except (NameError,SyntaxError,ValueError,TypeError):
            print "\nIntegers only for row and column values. Please try again!\n"
            continue
    
    #Checks for Treaure found or near
    if board[row][column] == 'T':
        print "\nYES!  You found a treasure.\n"
        board[row][column] = "$"
        return True
    else :
        if radar(board,row,column):
            print "\nVery close, treasure is near...\n"
            board[row][column] = "!"
        else:
            print "\nNothing there."
            board[row][column] = "X" 
        return False

main()