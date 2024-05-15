import math
import random
import itertools
import copy
import time
ROWS = 10
COLUMNS = 10
MINE_COUNT = 10

BOARD = []
MINES = set()
EXTENDED = set()

MATRIX = [['?'] * COLUMNS for i in range(ROWS)]
FLAGGED_MINES = set()

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
            if proposed_index is None:
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


def check_completed_square(i, j):
    num_mines = MATRIX[i][j]
    num,adjacent_squares_list = adjacent_squares(i, j)
    flagged_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if get_index(x, y) in FLAGGED_MINES]
    not_flagged_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if get_index(x, y) not in FLAGGED_MINES]
    if len(flagged_adjacent_squares) == num_mines:
        for limp_square in not_flagged_adjacent_squares:
            x,y = limp_square
            if MATRIX[x][y] == "?":

                print("square a limpiar ",i,j," y va a aquitar a ",limp_square)
                
                mine_hit = update_board(limp_square)
                #print(draw_board())
                if mine_hit or has_won():
                    if mine_hit:
                        reveal_mines()
                        #print(draw_board())
                        print('Game over')
                        return limp_square
                        
                        
                    else:
                        #print(draw_board())
                        print('You won!')
                        return limp_square
    return not_flagged_adjacent_squares[0]
                    

def detect_mines():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    # Check if any square adjacent to a revealed square has the same number of surrounding unrevealed squares as its number
    for square in options:
        i, j = square
        num_mines, adjacent_squares_list = adjacent_squares(i, j)
        revealed_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] != '?']
        for adj_square in revealed_adjacent_squares:
            adj_i, adj_j = adj_square
            adj_num_mines, adj_adjacent_squares_list = adjacent_squares(adj_i, adj_j)
            unknown_adjacent_squares = [(x, y) for x, y in adj_adjacent_squares_list if MATRIX[x][y] == '?']
            if len(unknown_adjacent_squares) == adj_num_mines and len(unknown_adjacent_squares) >0 and get_index(*square) not in FLAGGED_MINES:
                text = colorize(f'Flagging square {square} as a suspected mine',Colors.RED)
                print(text)
                FLAGGED_MINES.add(get_index(*square))


def Combination_player():
    detect_mines()
    
    safe_squares = []
    unknown_squares = []

    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                unknown_squares.append((i, j))
            else:
                completed_square = check_completed_square(i, j)
                if completed_square:
                    safe_squares.append(completed_square)

    if has_won():
        return safe_squares[0]
    detect_mines()
    # If no safe squares were found using direct checks, use combinations to deduce safe moves
    for combination_size in range(1, len(unknown_squares) + 1):
        for combination in itertools.combinations(unknown_squares, combination_size):
            if is_valid_combination(combination):
                for square in combination:
                    if get_index(*square) not in FLAGGED_MINES:
                        return square
    
    # If no deductions can be made, fallback to a random move
    return random_player()

def is_valid_combination(combination):
    # Placeholder function to check if a given combination is valid
    # A combination is valid if it satisfies all known clues on the board
    # For simplicity, let's assume every combination is valid in this placeholder
    # In practice, this function needs to validate the combination against all revealed clues
    return True





# def random_player():
#     options = []
#     for i in range(ROWS):
#         for j in range(COLUMNS):
#             if MATRIX[i][j] == '?':
#                 options.append((i, j))
#     rand_square = options[random.randint(0, len(options))]
#     print(f'Random player plays {rand_square}')
#     return rand_square

def random_player():
    options = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?']
    if not options:
        return None
    rand_square = random.choice(options)
    print(f'Random player plays {rand_square}')
    return rand_square

def run_simulation():
    start_time = time.time()  # Registra el tiempo inicial
    # Restablecer todas las estructuras de datos del tablero
    BOARD.clear()
    MINES.clear()
    EXTENDED.clear()
    FLAGGED_MINES.clear()
    for i in range(ROWS):
        for j in range(COLUMNS):
            MATRIX[i][j] = '?'
    create_board()

    print('First move by random player')
    random_square = random_player()
    update_board(random_square)
    mine_hit = update_board(random_square)
    print(draw_board())
    if mine_hit or has_won():
        if mine_hit:
            reveal_mines()
            print(draw_board())
            print('Game over')
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            return 'lost', elapsed_time
        else:
            print(draw_board())
            print('You won!')
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            return 'won', elapsed_time

    while True:
        # Heuristic player's turn
        square = Combination_player()
        print(f"Plays at: {square}")
        mine_hit = update_board(square)
        #print(draw_board())
        if mine_hit or has_won():
            if mine_hit:
                reveal_mines()
                print(draw_board())
                print('Game over')
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                return 'lost', elapsed_time
            else:
                print(draw_board())
                print('You won!')
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                return 'won', elapsed_time

# Ejecuta la simulación 100 veces y registra los resultados
with open("resultadosComb.txt", "w") as file:
    for i in range(100):
        print(f"\nSimulation {i + 1}")
        resultado, tiempo = run_simulation()
        file.write(f"Simulation {i + 1}: {resultado}, Time: {tiempo} seconds\n")