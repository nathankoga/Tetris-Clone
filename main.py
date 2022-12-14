# Use controller model and view???? Maybe
# Make a Minesweeper game / AI??????
# Snake too
# App next (maybe rubik's cube app)
# closest numbers, reduce the array, find the substring
import pygame
import random


# GLOBALS VARS
s_width = 800  # width of the game window
s_height = 700  # height of game window
play_width = 300  # playable board width
play_height = 600  # playable board height
block_size = 30  # 10 blocks in width

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
"""
pygame.font.init()

# SHAPE FORMATS, list of lists for each orientation

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # corresponds to index of shape rotation


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for col in range(10)] for row in range(20)]

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (col, row) in locked_pos:
                c = locked_pos[(col, row)]
                grid[row][col] = c
    return grid


def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]  # set number of rotations possible, mod (len).

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':  # found a block
                positions.append((shape.x + j, shape.y + i))  # shape.x/y to find current position on board

    # Offset the displaying of blocks up 4, left 2
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # Blocks fall from above the visible board

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [tup for lst in accepted_pos for tup in lst]  # 2D list to 1D, embedded lists to tuples

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))  # make random shape of the piece class


def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return int(score)


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('Segoe UI', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width()/2,
                         top_left_y + play_height / 2 - label.get_height()/2))


def draw_grid(surface, grid):
    # draws the lines of grid
    start_x = top_left_x
    start_y = top_left_y

    for row in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (start_x, start_y + row*block_size), (start_x + play_width,
                                                                                   start_y+row*block_size))
        for col in range(len(grid[row])):
            pygame.draw.line(surface, (128, 128, 128), (start_x + col*block_size, start_y), (start_x + col*block_size,
                                                                                             start_y + play_height))


def clear_rows(grid, locked):
    # calculated bottom up, hence increment by -1
    rows_removed = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            rows_removed += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if rows_removed > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:  # backwards so we don't overwrite previous clears
            x, y = key
            if y < ind:
                new_key = (x, y + rows_removed)
                locked[new_key] = locked.pop(key)

    return rows_removed  # return for score


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Segoe UI', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 55
    start_y = top_left_y + play_height/2 - 200
    formatted = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x + j*block_size, start_y + i*block_size,
                                                        block_size, block_size), 0)

    surface.blit(label, (start_x + 15, start_y - 40))


def draw_window(surface, grid, score=0, high_score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Segoe UI', 50)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('Segoe UI', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 55
    start_y = top_left_y + play_height / 2 - 100

    surface.blit(label, (start_x + 20, start_y + 180))

    # high score
    label = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))

    start_x = top_left_x + - 200
    start_y = top_left_y + + 200

    surface.blit(label, (start_x + 10, start_y + 180))

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col],
                             (top_left_x + col*block_size, top_left_y + row*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)  # playing window

    draw_grid(surface, grid)


def main(win):
    high_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.20
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                level_time -= 0.006

        if fall_time/ 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:  # piece moves down through piece/ board
                current_piece.y -= 1  # set piece to proper spot
                change_piece = True  # then change piece

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:  #
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color  # ex {(0,1): (255, 0, 0)}
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100

        draw_window(win, grid, score, high_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST!", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key To Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game




