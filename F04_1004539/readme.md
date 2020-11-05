<h1>The Game Name: Snake </h1>
Game Goal: <br>
To eat as many fruits as possible to elongate the snake and get a higher score.
Hitting the wall, hitting any stone and eating itself will cause to snake to die. <br><br>
Game Mods:<br>     
1.Speed mod: The snake will move faster each time it eats a fruit. <br>
2.Stone mod: Two stones will be randomly generated each time the snake eats a fruit.<br><br>
Game symbol:<br>
'#': wall or stone<br>
'@': the snake's head<br>
'*': the snake's body<br>
'o': fruit<br><br>

Game control:<br> 
1. In the main menu, press '1' or '2' to select either speed mod or stone mod. <br>
2. In the game, use "wasd" to control the snake to move upward, toward left, downward and toward right.<br>
3. Use 'q' to quit the current game and return to the main menu. Use 'r' to restart the current game
You can do this either in the middle of a game or when the game is over.<br>

Code description:
1. Class Cord is used to represent the position(which row which column) of a single character on the screen<br>
2. Class Snake keeps track of the snake and provides useful functions. <br>
3. Class SnakeState inherited from sm.SM keeps track of the direction of the snake(up/down/left/right).
   It is used to filter out the invalid keyboard input and handle the cases in which the input direction is opposite to the snake's current direction<br>
4. Class ModStates inherited from sm.SM determines whether the program is under main menu, speed mod or stone mod.
   It also outputs functions to handle the keyboard input under different states to make the main function much simpler<br>
5. Main function will run the function outputted by mod_state. This function will return the user's choice. (return to 
   main menu/ play speed mod/ restart the current game....) The return value will then be the input of mod_state and it will 
   again generate another function. This process forms a loop so that the program will keep running until the user closes it.<br>

[Video Link](https://www.youtube.com/watch?v=yaI8YyxG0X0)<br>

Code dependency: Unix-like operating system. (Windows do not have the module
 "curses" even though it is in Python Standard Lib)<br><br>
How to run the game:<br>
Open terminal under **full screen**(important!)<br>
cd to the directory which snake.py lies in.<br>
type "python snake.py" + Enter

                    
