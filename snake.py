import curses
from libdw import sm
import time
import random


#coodinate class to keep track of the position
class Cord(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        row = self.row + other.row
        col = self.col + other.col
        return Cord(row, col)

    def __eq__(self, other):
        return self.row==other.row and self.col==other.col


class Snake(object):
    def __init__(self, is_stone_mod=False, width=40, height=40):
        # Due to the height and width difference of a single character,
        # the time intervals to move vertically and horizontally are different
        self.vertical_speed = 0.14
        self.horizontal_speed = 0.08
        #Flag to indicate what is the current mod
        self.is_stone_mod = is_stone_mod
        #size of the wall
        self.width = width
        self.height = height
        #In stone mod, keep track of the coordinates of all the stones.
        #Empyty in speed mod
        self.stone = []
        #current score
        self.score = 0
        # Keep track of the coordinates of each character of the snake
        # The last element is the coordinate of the snake's head
        self.snake = []
        #highrst score
        self.highest = 0
        #Diretion vector to calculate the position of the new head based on the current head
        self.d_vector = dict(zip(['w', 's', 'a', 'd'], [Cord(-1, 0), Cord(1, 0), Cord(0, -1), Cord(0, 1)]))
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        self.restart()

    def set_stone_mod(self, b):
        self.is_stone_mod = b

    def restart(self):
        self.stdscr.clear()
        self.score = 0
        self.draw_bondary()
        self.draw_info()
        self.init_snake()
        self.draw_snake()
        self.generate_next_fruit()
        self.draw_fruit()
        if self.is_stone_mod:
            self.stone = []
            self.generate_stone()
            self.draw_stone()
        self.vertical_speed = 0.14
        self.horizontal_speed = 0.08

    #display the mod menu
    def display_mod_select(self):
        self.restart()
        self.stdscr.addstr(self.height//2, 4, 'Press 1(speed_mod) / 2(stone_mod)')
        #self.stdscr.addstr(self.height//2+1, 12, 'Press q to quit')

    def draw_bondary(self):
        self.stdscr.addstr(0, 0, '#'*self.width)
        self.stdscr.addstr(self.height-1, 0, '#'*self.width)
        for i in range(0, self.height):
            self.stdscr.addstr(i, 0, '#')
        for i in range(0, self.height):
            self.stdscr.addstr(i, self.width-1, '#')

    def draw_info(self):
        s = 'Current Score: ' + str(self.score) + ' Highest Score: ' + str(self.highest)
        self.stdscr.addstr(0, 0, s)

    def init_snake(self):
        self.snake = []
        for i in range(1, 6):
            self.snake.append(Cord(self.height//2, i))
        self.stdscr.addstr(self.height//2, 2, '***@')

    def draw_head(self):
        head = self.snake[-1]
        second = self.snake[-2]
        self.stdscr.addstr(head.row, head.col, '@')
        self.stdscr.addstr(second.row, second.col, '*')

    # cut the tail of the snake after each movement
    def cut_tail(self):
        del self.snake[0]

    def draw_snake(self):
        self.draw_head()
        last = self.snake[0]
        self.stdscr.addstr(last.row, last.col, ' ')

    def generate_next_fruit(self):
        while True:
            row = random.randrange(1, 39)
            col = random.randrange(1, 39)
            Pos = Cord(row, col)
            if Pos not in self.snake and Pos not in self.stone:
                break
        self.fruit = Pos

    def draw_fruit(self):
        self.stdscr.addstr(self.fruit.row, self.fruit.col, 'o')

    def generate_stone(self):
        num = 0
        while num < 2:
            row = random.randrange(1, 39)
            col = random.randrange(1, 39)
            Pos = Cord(row, col)
            if Pos not in self.snake and Pos != self.fruit and Pos not in self.stone:
                self.stone.append(Pos)
                num+=1

    def draw_stone(self):
        for stone in self.stone:
            self.stdscr.addstr(stone.row, stone.col, '#')

    def move(self, direction):
        #v is the direction vector used to calculate the next position of snake head
        v = self.d_vector[direction]
        #Coordinate of new head
        head = v+self.snake[-1]
        self.snake.append(head)
        if head != self.fruit:
            self.cut_tail()
        #If the head locates at the same position as the fruit
        else:
            self.score += 10
            self.highest = max(self.highest, self.score)
            #refresh the score board
            self.draw_info()
            self.generate_next_fruit()
            self.draw_fruit()
            #If it is under stone mod, generate 2 more stones
            if self.is_stone_mod:
                self.generate_stone()
                self.draw_stone()
            #If it is under speed mod, accelerate the snake's speed
            else:
                self.vertical_speed *= 0.95
                self.horizontal_speed *= 0.95
        self.draw_snake()

    def is_game_over(self):
        head = self.snake[-1]
        # head on the wall
        if head.row == 0 or head.col == 0 or head.row == 39 or head.col == 39:
            return True
        #eat itself or hit the stone
        if head in self.snake[:-1] or head in self.stone and self.is_stone_mod:
            return True
        return False

    def display_game_over(self):
        self.stdscr.addstr(self.height//2, 15, "Game Over")
        self.stdscr.addstr(self.height//2+1, 5, "Press Q(select mod)/R(restart)")

# stateMachine used to determine the next head direction
class SnakeStates(sm.SM):
    def __init__(self):
        self.start_state = 'd'
        self.state = self.start_state
        self.states = ['w', 's', 'a', 'd', 'q', 'r']
        self.opp_dir = dict(zip(['w', 's', 'a', 'd'], ['s', 'w', 'd', 'a']))

    def get_next_values(self, state, inp):
        assert isinstance(state, str)
        #if input char is not valid or there is no input
        if inp == -1 or chr(inp) not in self.states:
            return state, state
        #if the input direction is opposite to current direction, no change will happen
        #(The snake can not turn back in one move)
        if self.opp_dir.get(chr(inp)) == state:
            return state, state
        else:
            return chr(inp), chr(inp)

    def step(self, inp):
        self.state, res = self.get_next_values(self.state, inp)
        return res



snake = Snake()
#handle the keyboard input in mod menu
def mod_select():
    snake.display_mod_select()
    snake.stdscr.addstr(39, 39, '#')
    c = snake.stdscr.getch()
    while c not in [ord('1'), ord('2')]:
        c = snake.stdscr.getch()
    #speed mod
    return c

#handle the keyboard input and time interval in speed mod(is_stone_mod == False) and stone mod(is_stone_mod == True)
def mod(is_stone_mod):
    assert isinstance(snake, Snake)
    snake.set_stone_mod(is_stone_mod)
    snake.restart()
    direction = SnakeStates()
    while True:
        snake.stdscr.addstr(39, 39, '#')
        #snake.stdscr.getch() returns the unicode of the keyboard input
        #if there is no input, -1 will be returned
        c = snake.stdscr.getch()
        curr = direction.step(c)
        if curr == 'q':
            return ord('q')
        elif curr == 'r':
            return ord('r')
        else:
            snake.move(curr)
            if snake.is_game_over():
                snake.display_game_over()
                snake.stdscr.addstr(39, 39, '#')
                c = snake.stdscr.getch()
                while c not in [ord('q'), ord('r')]:
                    c = snake.stdscr.getch()
                return c
        if curr in ['w', 's']:
            time.sleep(snake.vertical_speed)
        else:
            time.sleep(snake.horizontal_speed)


speed_mod = lambda: mod(False)
stone_mod = lambda: mod(True)

#ModStates output different functions to handle the keyboard input
#change the state within ['mod_select', 'speed_mod', 'stone_mdo']
class ModStates(sm.SM):
    def __init__(self):
        self.start_state = 'mod_select'
        self.state = self.start_state

    def get_next_values(self, state, inp):
        if state == 'mod_select':
            # speed_mod：
            if inp == ord('1'):
                return 'speed_mod', speed_mod
            elif inp == ord('2'):
                return 'stone_mod', stone_mod
            else:
                return state, mod_select
        if state == 'speed_mod' or 'stone_mod':
            if inp == ord('r'):
                return state, speed_mod if state =='speed_mod' else stone_mod
            elif inp == ord('q'):
                return 'mod_select', mod_select

    def step(self, inp):
        self.state, res = self.get_next_values(self.state, inp)
        return res

def main():
    mod_state = ModStates()
    c = mod_select()
    while True:
        # The input value of the state machine is the return value from the last output function
        func = mod_state.step(c)
        c = func()
main()
