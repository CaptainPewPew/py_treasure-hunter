# py_treasure-hunter
This was originally a game made in python2 for Gr11 computer science class,
it has now been remade in PyGame with more funcationality.

# Functaionality

* Initialize Constants
    * initialize number of moves
    * initialize treasures number
    * initialize size of board --> put into board object
    * initialize size of Block --> put into Block object
* Initialize PyGame
    *
* Inistialize Needed Assets
* Display Game Start Screen ()
    * Start screen selection (Start, Leader Board, Quit)
    * Wait for Player Input
* If Start is Picked
    * Display game board
        * Place Blocks and hide treasure
        * Place Player at top right corner of screen
    * Display Counters
    * hjkl moves the Player
    * Space will allow the player to 'dig'
    * q will quit the game
* If Leader Board is Picked
    * Display top ten on leader board
    * Load using SQL queries
    * Wait for player input to go back
* If Quit is Picked
    * Quit Game

When Player 'digs'
* check if the block selected has treasure
    * if no treasure game will check if there's treasures around
        * if there is threasure around it will show the number of treasures around the Block
    * if there is no treasure around it will show ?
    * if treasure is found 'T' will show
* Check win lose condition
    * When all moves are used up the game will end
    * When all treasre is found it the game will end
        * if player wins then score will be added to database (time and moves)

CLASSes
* Game menus with different game loop (3 main game loop as methods in App Class)?
    * Main Game Loop
    * Start Menu
    * Leader Board
* Blocks
* Player



#TODO
[x] vim key binding for moving the cursor
    [x] Keyboard centric controll
    [ ] but also allow for mouse control -> Might be a bit hard to implement
[x] GUI
    [x] graphics (sprite)
[ ] using SQL to handle scoreboard
    [ ] different scoreboard for different difficulty (3 difficulty)
    [ ] record time and moves made
    [ ] do not need to record the name (kind of like old arcade games)
[ ] Add music and sound effects
[ ] rebalance the game (3 difficulty?)
