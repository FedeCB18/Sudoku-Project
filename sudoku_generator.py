import math, random
import pygame as pg


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = self.get_board()
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return [["-" for i in range(self.row_length)]
                for j in range(self.row_length)]

    def print_board(self):
        for row in self.board:
            for col in row:
                print(col, end=" ")
            print()

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        return True

    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(self.box_length):
            for j in range(self.box_length):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        row_start, col_start = self.box_start_coords(row, col)
        return (self.valid_in_row(row, num) and self.valid_in_col(col, num)
                and self.valid_in_box(row_start, col_start, num))

    def box_start_coords(self, row, col):
        row_start = row - row % self.box_length
        col_start = col - col % self.box_length
        return row_start, col_start

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_box(self, row_start, col_start):
        nums = random.sample(range(1, self.row_length + 1), self.row_length)
        z = 0
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = nums[z]
                z += 1

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)

            if self.board[row][col] != "-":
                self.board[row][col] = "-"
                removed += 1
              


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board





if __name__ == '__main__':
    sudoku = SudokuGenerator(9, 10)

    sudoku.print_board()
    print()
    sudoku.fill_diagonal()
    sudoku.print_board()
    print()
    sudoku.fill_values()
    sudoku.print_board()
    print()
    sudoku.remove_cells()
    sudoku.print_board()
