import pygame as pg
from cell import Cell
from constants import *
from sudoku_generator import generate_sudoku


class Board:

    def __init__(self, width, height, screen, generated_board):

        self.width = width
        self.height = height
        self.screen = screen
        self.rows = len(generated_board)
        self.cols = len(generated_board[0])
        self.square_size = self.width // self.rows
        self.values = generated_board
        self.locked_cells = self.get_locked_cells()
        self.selected = None

        self.cells = [[
            Cell(
                self.values[i][j],
                i,
                j,
                self.screen,
                locked=(i, j) in self.locked_cells,
            ) for j in range(self.cols)
        ] for i in range(self.rows)]

        self.original_values = [[self.values[i][j] for j in range(self.cols)]
                                for i in range(self.rows)]

    # ... rest of the Board class

    def draw(self):
        # Draw the grid
        for i in range(self.cols + 1):
            if i % 3 == 0:
                line_thickness = MAIN_LINE_WIDTH
            else:
                line_thickness = LINE_WIDTH
            pg.draw.line(self.screen, LINE_COLOR, (i * self.square_size, 0),
                         (i * self.square_size, self.height), line_thickness)
            pg.draw.line(self.screen, LINE_COLOR, (0, i * self.square_size),
                         (self.width, i * self.square_size), line_thickness)

        # Draw the cells
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def click(self, x, y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return None
        row = y // CELL_SQUARE_SIZE
        col = x // CELL_SQUARE_SIZE
        return row, col

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value != self.original_values[row][col]:
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        row, col = self.selected
        self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):  # Add value as an argument here
        if self.selected:
            row, col = self.selected
            cell = self.cells[row][col]
            if cell.value == 0:
                cell.set_cell_value(
                    value)  # Replace cell.value with value here
                cell.set_sketched_value(0)

    def reset_to_original(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].set_cell_value(
                    self.original_values[row][col])

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.values[row][col] = self.cells[row][col].value

    def find_empty(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self):
        # Check rows
        for row in self.values:
            if not self.check_set(row):
                return False

        # Check columns
        for col in range(self.cols):
            col_values = [self.values[row][col] for row in range(self.rows)]
            if not self.check_set(col_values):
                return False

        # Check boxes
        for row in range(0, self.rows, 3):
            for col in range(0, self.cols, 3):
                box_values = [
                    self.values[i][j] for i in range(row, row + 3)
                    for j in range(col, col + 3)
                ]
                if not self.check_set(box_values):
                    return False

        return True

    def check_set(self, values):
        return sorted(values) == list(range(1, 10))

    def get_locked_cells(self):
        locked = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.values[i][j] != 0:
                    locked.append((i, j))
        return locked
