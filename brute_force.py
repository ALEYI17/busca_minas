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


def Combination_player():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    
    # Iterate over combinations and check for a winning move
    for r in range(1, len(options) + 1):
        # Generate combinations of size 'r' and iterate over them
        for combination in itertools.combinations(options, r):
            # Track changes made by the current combination
            for move in combination:
                update_board(move, selected=False)
                if has_won():
                    # If a winning move is found, revert other moves and return the winning move
                    print(f'Combination player plays {combination}')
                    for other_move in combination:
                        if other_move != move:
                            i, j = other_move
                            MATRIX[i][j] = '?'
                    return move
                else:
                    # Revert the move since it didn't lead to a win
                    i, j = move
                    MATRIX[i][j] = '?'
    
    # If no winning move is found, return None
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

# if __name__ == '__main__':
#     create_board()

#     print('Enter coordinates (ie: 0 3)')
#     first_play = True

#     while True:

#         print(draw_board())
#         if first_play:
#           square = random_player()
#           first_play = False
#         else:
#           square = Combination_player()

#         if not square or len(square) < 2:
#             print('Unable to parse indicies, try again...')
#             break

#         mine_hit = update_board(square)
#         if mine_hit or has_won():
#             if mine_hit:
#                 reveal_mines()
#                 print(draw_board())
#                 print('Game over')
#             else:
#                 print(draw_board())
#                 print('You won!')
#             break

def run_simulation():
    start_time = time.time()  # Registra el tiempo inicial
    # Restablecer todas las estructuras de datos del tablero
    BOARD.clear()
    MINES.clear()
    EXTENDED.clear()
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