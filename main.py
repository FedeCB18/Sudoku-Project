import pygame as pg
from sudoku_generator import SudokuGenerator

# Constants
WIDTH, HEIGHT = 600, 700
WHITE = (255, 255, 255)
BLUE = (210, 231, 244)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
ORANGE = (243, 117, 0)
BROWN = (165, 93, 45)
RED = (255, 0, 0)
FONT_SIZE = 40
MENU_FONT_SIZE = 60
MENU_FONT_SIZE2 = 40
MENU_FONT_SIZE3 = 35
BUTTON_FONT_SIZE = 30
WELCOME_FONT_SIZE = 80

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Sudoku')
bg_image = pg.image.load("image.jpg").convert()
bg_image = pg.transform.scale(
  bg_image, (WIDTH, HEIGHT))  # Scale the image to fit the screen
clock = pg.time.Clock()
font = pg.font.Font(None, FONT_SIZE)
menu_font = pg.font.Font(None, MENU_FONT_SIZE)
menu_font2 = pg.font.Font(None, MENU_FONT_SIZE2)
menu_font3 = pg.font.Font(None, MENU_FONT_SIZE3)
button_font = pg.font.Font(None, BUTTON_FONT_SIZE)
welcome_font = pg.font.Font(None, WELCOME_FONT_SIZE)
winner = 1
running = True


def draw_board(sudoku, selected=None, temp_numbers=None):

  if temp_numbers is None:
    temp_numbers = [['' for _ in range(9)] for _ in range(9)]
  cell_size = WIDTH // 9
  for i in range(10):
    line_width = 4 if i % 3 == 0 else 1
    pg.draw.line(screen, BLACK, (i * cell_size, 0),
                 (i * cell_size, HEIGHT - 100), line_width)
    pg.draw.line(screen, BLACK, (0, i * cell_size), (WIDTH, i * cell_size),
                 line_width)
  board = sudoku.board
  cell_size = WIDTH // sudoku.row_length
  for row_idx, row in enumerate(board):
    for col_idx, col in enumerate(row):
      x, y = col_idx * cell_size, row_idx * cell_size
      pg.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 1)

      if selected == (row_idx, col_idx):
        pg.draw.rect(screen, RED, (x, y, cell_size, cell_size))
        pg.draw.rect(screen, BLUE,
                     (x + 3, y + 3, cell_size - 6, cell_size - 6))

      if col != '-':
        text = font.render(str(col), True, BLACK)
      else:
        if selected == (row_idx, col_idx) and temp_numbers[row_idx][col_idx]:
          text = font.render(str(temp_numbers[row_idx][col_idx]), True, BLACK)
        else:
          text = None

      if text is not None:
        text_rect = text.get_rect(center=(x + cell_size // 2,
                                          y + cell_size // 2))
        screen.blit(text, text_rect)

      # Display temporary numbers
      if temp_numbers[row_idx][col_idx] and col == '-':
        temp_text = font.render(str(temp_numbers[row_idx][col_idx]), True,
                                GRAY)
        temp_text_rect = temp_text.get_rect(topleft=(x + 5, y + 5))
        screen.blit(temp_text, temp_text_rect)


def get_cell_pos(mouse_x, mouse_y, sudoku):
  cell_size = WIDTH // sudoku.row_length
  row = mouse_y // cell_size
  col = mouse_x // cell_size
  return row, col


def display_welcome_text():
  welcome_text = welcome_font.render("Welcome to Sudoku", True, BLACK)
  welcome_text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 7))

  subheading_text = menu_font.render("Select Game Mode:", True, BLACK)
  subheading_text_rect = subheading_text.get_rect(center=(WIDTH // 2,
                                                          HEIGHT // 2.25))

  return welcome_text, welcome_text_rect, subheading_text, subheading_text_rect


def is_board_solved(sudoku):
  for row_idx, row in enumerate(sudoku.board):
    for col_idx, col in enumerate(row):
      if col == '-' or not sudoku.is_valid(row_idx, col_idx, col):
        return False
  return True


def is_board_completed(sudoku):
  for row in sudoku.board:
    for col in row:
      if col == '-':
        return False
  return True


def display_end_screen(win):
  screen.blit(bg_image, (0, 0))
  end_font = pg.font.Font(None, 80)
  end_text = "Game Won!" if win else "Game Over :("
  end_text_rendered = end_font.render(end_text, True, BLACK)
  text_rect = end_text_rendered.get_rect(center=(WIDTH // 2, HEIGHT // 3))
  screen.blit(end_text_rendered, text_rect)
  pg.display.flip()

  # Create button
  restart_button_rect = pg.Rect((WIDTH - 200) // 2, HEIGHT - 300, 200, 50)
  if (win):
    restart_button_text = button_font.render('EXIT', True, WHITE)
  else:
    restart_button_text = button_font.render('RESTART', True, WHITE)

  restart_button_text_rect = restart_button_text.get_rect(
    center=restart_button_rect.center)

  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        return
      elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_x, mouse_y):
          if (win == 0):
            main()
          else:
            running = False
          return

    # Draw button
    pg.draw.rect(screen, ORANGE, restart_button_rect)
    pg.draw.rect(screen, WHITE, restart_button_rect, 4)
    pg.draw.rect(screen, BROWN, restart_button_rect.inflate(4, 4), 4)
    screen.blit(restart_button_text, restart_button_text_rect)
    pg.display.flip()


def display_menu():
  menu_items = [('EASY', 30), ('MEDIUM', 40), ('HARD', 50)]
  menu_options = []
  spacing = 150
  for idx, (label, _) in enumerate(menu_items):
    text = menu_font3.render(label, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2 - spacing + idx * spacing,
                                      HEIGHT // 1.5))
    button_rect = pg.Rect(text_rect.left - 15, text_rect.top - 15,
                          text_rect.width + 30, text_rect.height + 30)
    menu_options.append((text, text_rect, button_rect))
  return menu_options


def get_difficulty(mouse_x, mouse_y, menu_options):
  for idx, (
      _, _,
      button_rect) in enumerate(menu_options):  # Unpack button_rect as well
    if button_rect.collidepoint(mouse_x, mouse_y):
      return idx
  return None


def create_buttons():
  button_labels = ['Reset', 'Restart', 'Exit']
  buttons = []
  button_width, button_height = 100, 50
  spacing = 20
  total_width = (button_width *
                 len(button_labels)) + (spacing * (len(button_labels) - 1))
  start_x = (WIDTH - total_width) // 2

  for idx, label in enumerate(button_labels):
    x = start_x + idx * (button_width + spacing)
    y = HEIGHT - button_height - spacing
    button_rect = pg.Rect(x, y, button_width, button_height)
    text = button_font.render(label, True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    buttons.append((button_rect, text, text_rect))
  return buttons


def check_button_click(mouse_x, mouse_y, buttons):
  for idx, (button_rect, _, _) in enumerate(buttons):
    if button_rect.collidepoint(mouse_x, mouse_y):
      return idx
  return None


def main():
  welcome_text, welcome_text_rect, subheading_text, subheading_text_rect = display_welcome_text(
  )

  menu_options = display_menu()
  difficulty = None
  temp_numbers = [['' for _ in range(9)] for _ in range(9)]

  while difficulty is None:
    winner = 1
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        return
      elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pg.mouse.get_pos()
        difficulty = get_difficulty(mouse_x, mouse_y, menu_options)

    screen.blit(bg_image, (0, 0))
    screen.blit(welcome_text, welcome_text_rect)
    screen.blit(welcome_text, welcome_text_rect)
    screen.blit(subheading_text, subheading_text_rect)

    for text, text_rect, button_rect in menu_options:

      pg.draw.rect(screen, ORANGE, button_rect)
      pg.draw.rect(screen, WHITE, button_rect, 4)
      pg.draw.rect(screen, BROWN, button_rect.inflate(4, 4), 4)
      screen.blit(text, text_rect)
    pg.display.flip()
    clock.tick(60)

  removed_cells = [30, 40, 50][difficulty]
  sudoku = SudokuGenerator(9, removed_cells)
  sudoku.fill_values()
  sudoku.remove_cells()
  initial_board = [row.copy() for row in sudoku.board]
  buttons = create_buttons()

  running = True
  selected = None
  input_number = None

  board_completed = False
  board_updated = False

  while running:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
      elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_y < 600 and not board_completed:
          selected = get_cell_pos(mouse_x, mouse_y, sudoku)
          if sudoku.board[selected[0]][selected[1]] != '-':
            selected = None

        button_clicked = check_button_click(mouse_x, mouse_y, buttons)
        if button_clicked == 0:  # Reset
          sudoku.board = [row.copy() for row in initial_board]

          board_completed = False
        elif button_clicked == 1:  # Restart

          main()
          return
        elif button_clicked == 2:  # Exit
          running = False

      elif event.type == pg.KEYDOWN:
        if selected is not None and sudoku.board[selected[0]][
            selected[1]] == '-' and not board_completed:
          if event.unicode.isdigit() and int(event.unicode) != 0:
            temp_number = int(event.unicode)
            temp_numbers[selected[0]][selected[1]] = temp_number
            board_updated = False
          elif event.key == pg.K_RETURN:
            temp_number = temp_numbers[selected[0]][selected[1]]
            if (sudoku.is_valid(selected[0], selected[1], temp_number)):
              sudoku.board[selected[0]][selected[1]] = temp_number
              temp_numbers[selected[0]][selected[1]] = ''
              board_updated = True
            elif temp_number:
              sudoku.board[selected[0]][selected[1]] = temp_number
              temp_numbers[selected[0]][selected[1]] = ''
              board_updated = True
              winner = 0

            #print(winner)

            if is_board_completed(sudoku):
              display_end_screen(winner)
              board_completed = True
              break

    screen.fill(BLUE)
    draw_board(sudoku, selected, temp_numbers)

    for button_rect, text, text_rect in buttons:
      pg.draw.rect(screen, ORANGE, button_rect)
      pg.draw.rect(screen, WHITE, button_rect, 4)
      pg.draw.rect(screen, BROWN, button_rect.inflate(4, 4), 4)
      screen.blit(text, text_rect)

    pg.display.flip()
    clock.tick(60)

    if board_completed:
      break

  pg.quit()


if __name__ == '__main__':
  main()
