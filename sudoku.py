import copy

sudoku_main = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 3, 6, 0, 0, 0, 0, 0],
               [0, 7, 0, 0, 9, 0, 2, 0, 0],
               [0, 5, 0, 0, 0, 7, 0, 0, 0],
               [0, 0, 0, 0, 4, 5, 7, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 3, 0],
               [0, 0, 1, 0, 0, 0, 0, 6, 8],
               [0, 0, 8, 5, 0, 0, 0, 1, 0],
               [0, 9, 0, 0, 0, 0, 4, 0, 0]]


def read_puzzle():
    print("Enter known numbers (enter dash for unknowns).")
    puzzle = []
    for i in range(1, 10):
        row = input("Row {}:".format(i))
        row = row.replace(",", "").replace(" ", "").replace("-", "0")
        assert len(row) == 9
        puzzle.append([digit for digit in row])
    return puzzle


def sudoku_to_str(sudoku):
    sudoku_str = ""
    for x in range(9):
        for y in range(9):
            number = sudoku[x][y]
            if number == 0:
                sudoku_str += "-"
            else:
                sudoku_str += str(sudoku[x][y])

                if (x != 2 or x != 5) and (y == 2 or y == 5):
                    sudoku_str += " |"
                if y == 8:
                    sudoku_str += "\n"
                else:
                    sudoku_str += " "

                if (x == 2 or x == 5) and y == 8:
                    sudoku_str += "- - - + - - - + - - - \n"

    return sudoku_str


def get_row(sudoku, index):
    return sudoku[index]


def get_column(sudoku, index):
    return [row[index] for row in sudoku]


def get_blox(sudoku, row, column):
    row *= 3
    column *= 3
    blox = []
    for x in range(row, row + 3):
        blox.extend(sudoku[x][column:column + 3])
    return blox


def get_possible_digits(sudoku, row, column):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    blox = get_blox(sudoku, row // 3, column // 3)
    row = get_row(sudoku, row)
    column = get_column(sudoku, column)
    impossible = list(set().union(blox, row, column))
    return [number for number in numbers if number not in impossible]


def get_score(sudoku):
    return 81 - sum([row.count(0) for row in sudoku])


def solve(sudoku, xy=(0, 0)):
    x = xy[0]
    y = xy[1]
    if sudoku[x][y] != 0:
        sudoku_copy = copy.deepcopy(sudoku)
        return solve(sudoku_copy, get_next((x, y)))
    else:
        digits = get_possible_digits(sudoku, x, y)
        for digit in digits:
            sudoku_copy = copy.deepcopy(sudoku)
            sudoku_copy[x][y] = digit
            if get_score(sudoku_copy) == 81:
                return sudoku_copy
            sudoku_copy = solve(sudoku_copy, get_next((x, y)))
            if get_score(sudoku_copy) == 81:
                return sudoku_copy
    return sudoku


def get_next(xy):
    x = xy[0]
    y = xy[1]
    next_y = (y + 1) % 9
    next_x = x + 1 if next_y < y else x
    return (next_x, next_y)


print(sudoku_to_str(solve(sudoku_main)))
