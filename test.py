
import itertools
import random
import unittest
FLAGGED_MINES = set()
ROWS = 4
COLUMNS = 4
MATRIX = [
            ['1', '1', '1', '?'],
            ['1', '?', '1', '?'],
            ['1', '1', '1', '?'],
            ['?', '?', '?', '?']
        ]
MINES = set()


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
def get_index(i, j):
    if 0 > i or i >= COLUMNS or 0 > j or j >= ROWS:
        return None
    return i * ROWS + j

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
                
                FLAGGED_MINES.add(get_index(*square))

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
                return limp_square
    return not_flagged_adjacent_squares[0]

def information_gained_algorithm():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] != '?':
                options.append((i, j))
    information_gain = {}
    for square in options:
        if get_index(*square) not in FLAGGED_MINES:
            i, j = square
            num_mines, adjacent_squares_list = adjacent_squares(i, j)
            unknown_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] == '?']
            information_gain[square] = len(unknown_adjacent_squares)
    sorted_information_gain = sorted(information_gain.items(), key=lambda x: x[1])
    sorted_information_gain = [(square, gain) for square, gain in sorted_information_gain if gain != 0]
    return sorted_information_gain
     
def find_play(sorted_information_gain,squ):
    selected_square = squ
    for square, gain in sorted_information_gain:
        
        num_mines, adjacent_squares_list = adjacent_squares(*square)
        unknown_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] == '?']

        for squad in unknown_adjacent_squares:
            if get_index(*squad) not in FLAGGED_MINES:
                selected_square = squad
                return selected_square
    return selected_square

def heuristic_player_directed():
    
    detect_mines()

    sorted_information_gain = information_gained_algorithm()
    selected_square = None
    for square , gain in sorted_information_gain:
        selected_square = check_completed_square(*square)
    
    detect_mines()
    
    
    sorted_information_gain = information_gained_algorithm()

    selected_square = find_play(sorted_information_gain, selected_square)

    if selected_square is None:
        # If there are no available squares to select, choose a random square that is not flagged as a mine
        available_squares = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?' and get_index(i, j) not in FLAGGED_MINES]
        if available_squares:
            selected_square = random.choice(available_squares)
            print(f'No available squares to select. Randomly choosing {selected_square}.')
        else:
            print("No available squares to select.")
    else:
        print(f'Heuristic player with directed exploration plays {selected_square}')

    return selected_square

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

def random_player():
    options = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?']
    if not options:
        return None
    rand_square = random.choice(options)
    print(f'Random player plays {rand_square}')
    return rand_square

def is_valid_combination(combination):

    return True
MINES.add(get_index(1, 1))

class TestCombinationPlayer(unittest.TestCase):

    def test_detect_mines(self):
        ROWS = 4
        COLUMNS = 4

        # Ejecutar la función detect_mines
        detect_mines()

        # Verificar si las minas se han marcado correctamente como sospechosas
        print("hola", FLAGGED_MINES)
        self.assertTrue(get_index(1, 1) in FLAGGED_MINES)  
        
        
        
    def test_check_completed_square(self):
        
        i, j = 1, 2
        detect_mines()
        # Ejecutar la función check_completed_square
        selected_square = check_completed_square(i, j)
        
        # Verificar si se selecciona correctamente el cuadrado a limpiar
        self.assertEqual(selected_square, (0, 1))

    def test_information_gained_algorithm(self):
        # Ejecutar la función information_gained_algorithm
        result = information_gained_algorithm()

       
        self.assertIsInstance(result, list)
        for square, gain in result:
            self.assertIsInstance(square, tuple)
            self.assertEqual(len(square), 2)
            self.assertIsInstance(gain, int)
            self.assertGreater(gain, 0)
            self.assertIn(((1, 2), 4), result)

    
    def test_find_play(self):
        # Definir datos de ejemplo
        sorted_information_gain = [((0, 0), 3), ((0, 1), 2), ((0, 2), 3), ((1, 0), 2), ((1, 2), 3), ((2, 0), 3), ((2, 1), 2), ((2, 2), 3)]
        selected_square = (1, 1)
        
        # Ejecutar la función find_play
        result = find_play(sorted_information_gain, selected_square)
        
        # Verificar si el resultado es del tipo esperado
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], int)
        self.assertEqual(result, (0,3))
        
    def test_heuristic_player_directed(self):
        # Ejecutar la función heuristic_player_directed
        selected_square = heuristic_player_directed()

        # Verificar si el cuadrado seleccionado es del tipo esperado
        self.assertIsInstance(selected_square, tuple)
        self.assertEqual(len(selected_square), 2)
        self.assertIsInstance(selected_square[0], int)
        self.assertIsInstance(selected_square[1], int)
    
    def test_Combination_player(self):
        # Ejecutar la función Combination_player
        selected_square = Combination_player()

        # Verificar si el cuadrado seleccionado es del tipo esperado
        if selected_square is not None:
            self.assertIsInstance(selected_square, tuple)
            self.assertEqual(len(selected_square), 2)
            self.assertIsInstance(selected_square[0], int)
            self.assertIsInstance(selected_square[1], int)


if __name__ == '__main__':
    unittest.main()
