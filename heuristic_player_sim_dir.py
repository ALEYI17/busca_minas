import math
import random
import time
ROWS = 10
COLUMNS = 10
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


# def heuristic_player():
#     options = []
#     for i in range(ROWS):
#         for j in range(COLUMNS):
#             if MATRIX[i][j] == '?':
#                 options.append((i, j))

#     # Prioritize squares based on the heuristic
#     prioritized_squares = []
#     for square in options:
#         i, j = square
#         num_mines, adjacent_squares_list = adjacent_squares(i, j)
#         unknown_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] == '?']
#         if num_mines == len(unknown_adjacent_squares):
#             # All adjacent mines are accounted for, prioritize this square
#             prioritized_squares.append(square)

#     # If there are prioritized squares, choose one randomly from them
#     if prioritized_squares:
#         selected_square = random.choice(prioritized_squares)
#         print(f'Heuristic player plays {selected_square}')
#         return selected_square
    
#     # If no prioritized squares, choose randomly from all options
#     rand_square = random.choice(options)
#     print(f'Heuristic player plays random {rand_square}')
#     return rand_square

def heuristic_player_directed():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))

    # Calculate the information gain for each square
    information_gain = {}
    for square in options:
        i, j = square
        num_mines, adjacent_squares_list = adjacent_squares(i, j)
        unknown_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] == '?']
        information_gain[square] = len(unknown_adjacent_squares)

    # Choose the square with the highest information gain
    selected_square = max(information_gain, key=information_gain.get)
    print(f'Heuristic player with directed exploration plays {selected_square}')
    return selected_square


def random_player():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    
    if not options:
        print("No remaining options for random player!")
        return None

    rand_square = options[random.randint(0, len(options) - 1)]  # Ajuste para evitar IndexError
    print(f'Random player plays {rand_square}')
    return rand_square


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
        square = heuristic_player_directed()
        print(f"Juega en: {square}")
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
with open("resultados.txt", "w") as file:
    for i in range(100):
        print(f"\nSimulación {i + 1}")
        resultado, tiempo = run_simulation()
        file.write(f"Simulación {i + 1}: {resultado}, Tiempo: {tiempo} segundos\n")
