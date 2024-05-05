import math
import random
from itertools import combinations
ROWS = 10
COLUMNS = 10
MINE_COUNT = 10

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


def random_player():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    rand_square = options[random.randint(0, len(options))]
    print(f'Random player plays {rand_square}')
    return rand_square
    # NO SE PUEDE REVISAR  MINES!!!
    #TODO: 1. Combinaciones de opciones seleccionadas y no seleccionadas (fuerza bruta)
    #TODO: 2. Heurística: Revisar combinaciones promisorias



def generate_combinations():
    # Generate all combinations of coordinates
    all_coordinates = [(i, j) for i in range(ROWS) for j in range(COLUMNS)]
    return combinations(all_coordinates, MINE_COUNT)

def reset_board():
    global BOARD, EXTENDED, MATRIX
    BOARD = ['[ ]'] * (ROWS * COLUMNS)
    EXTENDED = set()
    MATRIX = [['?'] * COLUMNS for i in range(ROWS)]

def brute_force():
    combinations = generate_combinations()
    
    best_square = None
    best_score = float('-inf')  # Initialize with negative infinity
    
    # Iterate through all combinations
    for combination in combinations:
        # Reset the board to initial state for each combination
        reset_board()
        
        # Apply the current combination to the board
        for square in combination:
            update_board(square)
            # Check if the selected square hits a mine
            if update_board(square):
                break  # Move on to the next combination if a mine is hit
        
        # Evaluate the combination's potential score
        score = evaluate_combination(combination)
        
        # Update the best square and best score if the current combination is better
        if score > best_score:
            best_square = combination[0]  # Select the first square of the combination as the best square
            best_score = score
    
    # Return the best square found
    return best_square

def evaluate_combination(combination):
    # Evaluate the combination's potential score here
    # You can implement your own scoring function based on the game's logic
    # For example, you can consider factors like the number of revealed squares, number of unrevealed squares, etc.
    score = 0
    # Your scoring logic goes here...
    return score


if __name__ == '__main__':
    create_board()

    print('Enter coordinates (ie: 0 3)')

    # Make the first move using the random player
    random_square = random_player()
    mine_hit = update_board(random_square)

    if mine_hit or has_won():
        if mine_hit:
            reveal_mines()
            print(draw_board())
            print('Game over')
            exit()
  
            
    while True:
        print(draw_board())
        square = brute_force()
        mine_hit = update_board(square)
        if mine_hit or has_won():
            if mine_hit:
                reveal_mines()
                print(draw_board())
                print('Game over')
            else:
                print(draw_board())
                print('You won!')
            break
