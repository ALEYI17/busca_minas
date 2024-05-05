import math
import random
from itertools import combinations
ROWS = 5
COLUMNS = 5
MINE_COUNT = 5

BOARD = []
MINES = set()
EXTENDED = set()

MATRIX = [['?'] * COLUMNS for i in range(ROWS)]


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def colorize(s, color):
    return '{}{}{}'.format(color, s, Colors.ENDC)


def get_index(i, j):
    if 0 > i or i >= COLUMNS or 0 > j or j >= ROWS:
        return None
    return i * ROWS + j


def create_board():
    squares = ROWS * COLUMNS

    # Create board
    for _ in range(squares):
        BOARD.append('[ ]')

    # Create mines
    while True:
        if len(MINES) >= MINE_COUNT:
            break
        MINES.add(int(math.floor(random.random() * squares)))


def draw_board():
    lines = []

    for j in range(ROWS):
        if j == 0:
            lines.append('   ' + ''.join(' {} '.format(x) for x in range(COLUMNS)))

        line = [' {} '.format(j)]
        for i in range(COLUMNS):
            line.append(BOARD[get_index(i, j)])
        lines.append(''.join(line))

    return '\n'.join(reversed(lines))


def parse_selection(raw_selection):
    try:
        return [int(x.strip(','), 10) for x in raw_selection.split(' ')]
    except Exception:
        return None


def adjacent_squares(i, j):
    num_mines = 0
    squares_to_check = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            # Skip current square
            if di == dj == 0:
                continue

            coordinates = i + di, j + dj

            # Skip squares off the board
            proposed_index = get_index(*coordinates)
            if not proposed_index:
                continue

            if proposed_index in MINES:
                num_mines += 1

            squares_to_check.append(coordinates)

    return num_mines, squares_to_check


def update_board(square, selected=True):
    i, j = square
    index = get_index(i, j)
    EXTENDED.add(index)

    # Check if we hit a mine, and if it was selected by the user or merely traversed
    if index in MINES:
        if not selected:
            return
        BOARD[index] = colorize(' X ', Colors.RED)
        return True
    else:
        num_mines, squares = adjacent_squares(i, j)
        MATRIX[i][j] = num_mines
        if num_mines:
            if num_mines == 1:
                text = colorize(num_mines, Colors.BLUE)
            elif num_mines == 2:
                text = colorize(num_mines, Colors.GREEN)
            else:
                text = colorize(num_mines, Colors.RED)

            BOARD[index] = ' {} '.format(text)
            return
        else:
            BOARD[index] = '   '

            for asquare in squares:
                aindex = get_index(*asquare)
                if aindex in EXTENDED:
                    continue
                EXTENDED.add(aindex)
                update_board(asquare, False)


def reveal_mines():
    for index in MINES:
        if index in EXTENDED:
            continue
        BOARD[index] = colorize(' X ', Colors.YELLOW)


def has_won():
    return len(EXTENDED | MINES) == len(BOARD)


def brute_force_player(extended):
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))

    # Sort the options based on some heuristic (e.g., number of adjacent mines)
    options.sort(key=lambda square: len(adjacent_squares(square[0], square[1])[1]))

    # Generate all possible combinations of squares to select
    for r in range(1, len(options) + 1):
        for combination in combinations(options, r):
            extended_copy = extended.copy()
            for square in combination:
                i, j = square
                num_mines, _ = adjacent_squares(i, j)
                if num_mines > 0:
                    break
                update_board(square)
                if has_won():
                    return combination
            extended = extended_copy.copy()

    return None

def random_player():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    rand_square = options[random.randint(0, len(options))]
    print(f'Random player plays {rand_square}')
    return rand_square


if __name__ == '__main__':
    create_board()

    print('Enter coordinates (ie: 0 3)')

    # First move by random player
    random_square = random_player()
    update_board(random_square)



    while True:
        print(draw_board())
        square_to_select = brute_force_player(EXTENDED)
        if square_to_select:
            print('Brute-force player plays {}'.format(square_to_select))
            for square in square_to_select:
                print(f"Squeare: {square}")
                update_board(square)
        else:
            print("Brute-force player couldn't find a move.")
        
        if has_won():
            print(draw_board())
            print('You won!')
            break