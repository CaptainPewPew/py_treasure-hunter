'''Author: Lei Yu
   Last Date Edited: 2016/01/17
   Purpose: a treasure hunter game,displays hall of fame then asks for size of 
            game board, gives player 10 guesses to find 3 treasures that are
            randomly placed on the game board.
'''
import random

def main():
    print "WELCOME TO TREASURE HUNT!\n"
    display_hall_of_fame()
    
    board = []
    
    make_board(board)
    hide_treasure(board)
    
    treasures_found = 0    
    #gives 10 turn to player and displays game status information
    for guess in range(10,0,-1):
        if treasures_found == 3:
            break
        else :
            print "\nYou have %d guess left and have found %d/3 treasures.\n" %\
                  (guess,treasures_found)
            display_board(board)
            if make_user_move(board):
                treasures_found += 1
                
    #displays 'T' location
    display_board(board,True)
    #if player has won, player name is recorded in 'Winners.txt'
    if treasures_found == 3:
        print "CONGRATULATIONS!  You found ALL of the hidden treasure.\n"  
        record_winner()
    else :
        print "OH NO! You only found %d/3 treasures.\n" %(treasures_found)
    print "\n*** GAME OVER ***"
    
def display_hall_of_fame():
    '''displays halls of fame shows empty if Winners.txt not found or empty'''
    try :
        hall_of_fame = open('Winners.txt', 'r')
        print " Hall OF Fame "
        print "=============="
        for line in hall_of_fame:
            print line.strip().center(14)
        print "==============\n"
        hall_of_fame.close()
    except IOError:
        print " Hall OF Fame "
        print "=============="
        print "<-- Empty! -->"
        print "==============\n"

def record_winner():
    winner_name = raw_input("What's your name stranger? ")
    hall_of_fame = open("Winners.txt",'a')
    hall_of_fame.write(str(winner_name) + "\n")
    hall_of_fame.close()
    
def make_board(board):
    ''' asks user for size of board and makes one'''
    sublist = []
    while True:
        try :
            row = int(input("How many rows would you like (3-10): "))
            column = int(input("How many columns would you like (3-10): "))
        except (NameError,SyntaxError,TypeError) :
            print "\nInteger values only! Please try again.\n"
            continue
            
        if column >= 3 and column <= 10 and row >= 3 and row <= 10:
            break
        else :
            print "\nInvalid board size!! Please try again.\n"

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
    print ' ',
    for _ in range(len(board[0])):
            if _ == (len(board[0])-1):
                    print " %d " %(_)
                    break
            print " %d " %(_),
    #prints row #s and game board
    for row in range(len(board)):
            print str(row)+":",
            if show_treasure:
                print ' | '.join(board[row])
            else :
                print ' | '.join(board[row]).replace('T',' ')
            print '  ' + '+'.join(['---']*len(board[0]))
    print

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
            row = input("What row would you like to search (0-%d): " %(len(board)-1))
            column = input("What col would you like to search (0-%d): " %(len(board[0])-1)) 
            if row <= (len(board)-1) and row >= 0 and column <= (len(board[0])-1) and column >= 0:
            #checks if board index has been checked
                if board[row][column] == ' ' or board[row][column] == 'T':
                    move = False
                else :
                    print "\nYou already tried there, please pick again.\n"
            else :
                print "\nSorry, invalid location. Please try again!\n"
        except (NameError,SyntaxError,TypeError,ValueError):
            print "\nIntegers only for row and column values. Please try again!\n"
            continue

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