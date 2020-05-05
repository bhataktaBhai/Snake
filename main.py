from tkinter import *
from random import randint


class Snake(Tk):

    ROWS = 21
    COLUMNS = 31
    WIDTH = 20
    PADDING = 3

    WRAP = False
    TIME_PER_MOVE = 40  # milliseconds

    SNAKE_COLOUR = 'GREEN4'
    FOOD_COLOUR = 'SADDLE BROWN'
    BACKGROUND_COLOUR = 'BLACK'

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry(f'{self.COLUMNS*self.WIDTH}x{(self.ROWS+1)*self.WIDTH}')
        self.resizable(0, 0)
        self.grid_propagate(False)
        self.config(background = self.BACKGROUND_COLOUR)
        self.squares = [[None]*self.COLUMNS for y in range(self.ROWS)]
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                square = Frame(self, background = self.BACKGROUND_COLOUR,
                               height = self.WIDTH - 2*self.PADDING,
                               width  = self.WIDTH - 2*self.PADDING)
                square.grid(row = row, column = column,
                            padx = self.PADDING,
                            pady = self.PADDING,
                            sticky = N + S + W + E)
                self.squares[row][column] = square
        self.score = self.high_score = self.keys = 0
        self.score_text = StringVar()
        self.high_score_text = StringVar()
        self.message = StringVar()
        frame = Frame(self, width = self.COLUMNS*self.WIDTH, height = self.WIDTH)
        self.score_box = Label(master = frame,
                               textvariable = self.score_text)
        self.high_score_box = Label(master = frame,
                                    textvariable = self.high_score_text)
        self.message_box = Label(master = frame,
                                 textvariable = self.message)
        self.high_score_box.pack(side = LEFT, fill = Y)
        self.score_box.pack(side = RIGHT, fill = Y)
        self.message_box.pack(side = BOTTOM, fill = BOTH, expand = True)
        frame.grid(row = self.ROWS, column = 0,
                   columnspan = self.COLUMNS)
        frame.pack_propagate(0)
        self.snake = []
        self.direction = ()
        self.start()

    def start(self):
        self.score_box.config(background = 'WHITE', foreground = 'BLACK')
        self.high_score_box.config(background = 'WHITE', foreground = 'BLACK')
        self.message_box.config(background = 'WHITE', foreground = 'BLACK')
        self.score_text.set(value = 'SCORE: 0')
        self.high_score_text.set(value = f'HIGH SCORE: {self.high_score}')
        self.message.set(value = 'Arrow Keys to Move')
        mid_row = self.ROWS // 2
        self.snake = [(mid_row, column) for column in range(self.COLUMNS//2 + 3, self.COLUMNS//2 - 2, -1)]
        self.keys = self.score = 0
        self.direction = (0, 1)
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                self.squares[row][column].config(bg = self.BACKGROUND_COLOUR)
        for row, column in self.snake:
            self.squares[row][column].config(bg = self.SNAKE_COLOUR)
        self.generate()
        self.bind('<Return>', lambda event: self.update( 0,  1, self.keys + 1, True))
        self.bind('<Right>' , lambda event: self.update( 0,  1, self.keys + 1, True))
        self.bind('<Left>'  , lambda event: self.update( 0, -1, self.keys + 1, True))
        self.bind('<Up>'    , lambda event: self.update(-1,  0, self.keys + 1, True))
        self.bind('<Down>'  , lambda event: self.update( 1,  0, self.keys + 1, True))

    def update(self, r_jump, c_jump, keys, key = False):
        if key:
            if (-r_jump, -c_jump) == self.direction:
                return
            self.direction = (r_jump, c_jump)
            self.keys = keys
        elif keys != self.keys:
            return
        tail_row, tail_column = self.snake[-1]
        self.squares[tail_row][tail_column].config(bg = self.BACKGROUND_COLOUR)
        head_row, head_column = self.snake[0]
        head_row += r_jump
        head_column += c_jump
        if not self.WRAP and (not 0 <= head_row < self.ROWS
                              or not 0 <= head_column < self.COLUMNS):
            self.snake = self.snake[:-1]
            self.defeat()
            return
        head_row = (head_row + self.ROWS) % self.ROWS
        head_column = (head_column + self.COLUMNS) % self.COLUMNS
        new_head = self.squares[head_row][head_column]
        if (head_row, head_column) in self.snake[:-1]:
            self.snake = [(head_row, head_column)] + self.snake
            self.defeat()
            return
        if new_head['bg'] == self.FOOD_COLOUR:
            self.snake = [(head_row, head_column)] + self.snake
            new_head.config(background = self.SNAKE_COLOUR)
            self.generate()
            self.score += 1
            self.score_text.set(f'SCORE: {self.score}')
        else:
            new_head.config(background = self.SNAKE_COLOUR)
            self.snake = [(head_row, head_column)] + self.snake[:-1]
        self.after(self.TIME_PER_MOVE, lambda: self.update(r_jump, c_jump, keys))

    def defeat(self):
        self.bind('<Return>', lambda event: self.start())
        self.bind('<Right>' , lambda event: 0)
        self.bind('<Left>'  , lambda event: 0)
        self.bind('<Up>'    , lambda event: 0)
        self.bind('<Down>'  , lambda event: 0)
        bite = self.snake[0]
        self.squares[bite[0]][bite[1]].config(background = 'DARK GREEN')
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_text.set(value = f'HIGH SCORE: {self.high_score}')
        self.message.set(value = 'Press Enter to Restart')
        self.score_box.config(background = 'RED', foreground = 'WHITE')
        self.message_box.config(background = 'RED', foreground = 'WHITE')
        self.high_score_box.config(background = 'RED', foreground = 'WHITE')

    def generate(self):
        row = randint(0, self.ROWS - 1)
        column = randint(0, self.COLUMNS - 1)
        if (row, column) in self.snake:
            self.generate()
            return
        self.squares[row][column].config(background = self.FOOD_COLOUR)


root = Snake(className = '---SNAKE---')
root.mainloop()
