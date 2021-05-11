--- TreasureHunt.py	(original)
+++ TreasureHunt.py	(refactored)
@@ -7,7 +7,7 @@
 import random
 
 def main():
-    print "WELCOME TO TREASURE HUNT!\n"
+    print("WELCOME TO TREASURE HUNT!\n")
     display_hall_of_fame()
     
     board = []
@@ -21,8 +21,8 @@
         if treasures_found == 3:
             break
         else :
-            print "\nYou have %d guess left and have found %d/3 treasures.\n" %\
-                  (guess,treasures_found)
+            print("\nYou have %d guess left and have found %d/3 treasures.\n" %\
+                  (guess,treasures_found))
             display_board(board)
             if make_user_move(board):
                 treasures_found += 1
@@ -31,30 +31,30 @@
     display_board(board,True)
     #if player has won, player name is recorded in 'Winners.txt'
     if treasures_found == 3:
-        print "CONGRATULATIONS!  You found ALL of the hidden treasure.\n"  
+        print("CONGRATULATIONS!  You found ALL of the hidden treasure.\n")  
         record_winner()
     else :
-        print "OH NO! You only found %d/3 treasures.\n" %(treasures_found)
-    print "\n*** GAME OVER ***"
+        print("OH NO! You only found %d/3 treasures.\n" %(treasures_found))
+    print("\n*** GAME OVER ***")
     
 def display_hall_of_fame():
     '''displays halls of fame shows empty if Winners.txt not found or empty'''
     try :
         hall_of_fame = open('Winners.txt', 'r')
-        print " Hall OF Fame "
-        print "=============="
+        print(" Hall OF Fame ")
+        print("==============")
         for line in hall_of_fame:
-            print line.strip().center(14)
-        print "==============\n"
+            print(line.strip().center(14))
+        print("==============\n")
         hall_of_fame.close()
     except IOError:
-        print " Hall OF Fame "
-        print "=============="
-        print "<-- Empty! -->"
-        print "==============\n"
+        print(" Hall OF Fame ")
+        print("==============")
+        print("<-- Empty! -->")
+        print("==============\n")
 
 def record_winner():
-    winner_name = raw_input("What's your name stranger? ")
+    winner_name = input("What's your name stranger? ")
     hall_of_fame = open("Winners.txt",'a')
     hall_of_fame.write(str(winner_name) + "\n")
     hall_of_fame.close()
@@ -64,16 +64,16 @@
     sublist = []
     while True:
         try :
-            row = int(input("How many rows would you like (3-10): "))
-            column = int(input("How many columns would you like (3-10): "))
+            row = int(eval(input("How many rows would you like (3-10): ")))
+            column = int(eval(input("How many columns would you like (3-10): ")))
         except (NameError,SyntaxError,TypeError) :
-            print "\nInteger values only! Please try again.\n"
+            print("\nInteger values only! Please try again.\n")
             continue
             
         if column >= 3 and column <= 10 and row >= 3 and row <= 10:
             break
         else :
-            print "\nInvalid board size!! Please try again.\n"
+            print("\nInvalid board size!! Please try again.\n")
 
     #modifies board with the amount of column and rows suggested by user
     for cols in range(column):
@@ -96,21 +96,21 @@
     '''displays game board, if show_treasure = True, 'T' are displayed, and vise
     versa, does not return any value'''
     #prints column #s
-    print ' ',
+    print(' ', end=' ')
     for _ in range(len(board[0])):
             if _ == (len(board[0])-1):
-                    print " %d " %(_)
+                    print(" %d " %(_))
                     break
-            print " %d " %(_),
+            print(" %d " %(_), end=' ')
     #prints row #s and game board
     for row in range(len(board)):
-            print str(row)+":",
+            print(str(row)+":", end=' ')
             if show_treasure:
-                print ' | '.join(board[row])
+                print(' | '.join(board[row]))
             else :
-                print ' | '.join(board[row]).replace('T',' ')
-            print '  ' + '+'.join(['---']*len(board[0]))
-    print
+                print(' | '.join(board[row]).replace('T',' '))
+            print('  ' + '+'.join(['---']*len(board[0])))
+    print()
 
 def radar(board,row,column):
     for row_set in [-1,0,1]:
@@ -129,30 +129,30 @@
     move = True
     while move:
         try :
-            row = input("What row would you like to search (0-%d): " %(len(board)-1))
-            column = input("What col would you like to search (0-%d): " %(len(board[0])-1)) 
+            row = eval(input("What row would you like to search (0-%d): " %(len(board)-1)))
+            column = eval(input("What col would you like to search (0-%d): " %(len(board[0])-1))) 
             if row <= (len(board)-1) and row >= 0 and column <= (len(board[0])-1) and column >= 0:
             #checks if board index has been checked
                 if board[row][column] == ' ' or board[row][column] == 'T':
                     move = False
                 else :
-                    print "\nYou already tried there, please pick again.\n"
+                    print("\nYou already tried there, please pick again.\n")
             else :
-                print "\nSorry, invalid location. Please try again!\n"
+                print("\nSorry, invalid location. Please try again!\n")
         except (NameError,SyntaxError,TypeError,ValueError):
-            print "\nIntegers only for row and column values. Please try again!\n"
+            print("\nIntegers only for row and column values. Please try again!\n")
             continue
 
     if board[row][column] == 'T':
-        print "\nYES!  You found a treasure.\n"
+        print("\nYES!  You found a treasure.\n")
         board[row][column] = "$"
         return True
     else :
         if radar(board,row,column):
-            print "\nVery close, treasure is near...\n"
+            print("\nVery close, treasure is near...\n")
             board[row][column] = "!"
         else:
-            print "\nNothing there."
+            print("\nNothing there.")
             board[row][column] = "X" 
         return False
 
