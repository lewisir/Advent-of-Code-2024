"""
--- Advent of Code 2024 ---
--- Day 4: Ceres Search ---
https://adventofcode.com/2024/day/4
"""

from time import perf_counter

TEST = False

DAY = "4"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

XMAS = "XMAS"
CHAR = "A"


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    xmas_count = 0
    for _ in range(4):
        data = rotate_word_search(data)
        for line in data:
            xmas_count += line.count(XMAS)
        strings = extract_diagonal_strings(data)
        for line in strings:
            xmas_count += line.count(XMAS)
    print(f"Part 1 - Word Count {xmas_count}")
    new_count = 0
    all_coordinates = find_char_coords(data, CHAR)
    focus_coordinates = filter_coordinates(data, all_coordinates)
    for coord in focus_coordinates:
        if test_for_x_mas(get_corners(data, coord[0], coord[1])):
            new_count += 1
    print(f"Part II - X-MAS Count {new_count}")


def rotate_word_search(text):
    """Take the block of text and rotate it 90 degrees)"""
    return ["".join(list(x)) for x in zip(*text[::-1])]


def extract_diagonal_strings(text):
    """From the block of text return a list of all the diagonal strings that can be produced"""
    height = len(text)
    width = len(text[0])
    output_strings = []
    for y in range(height):
        output_strings.append(get_diagonal_string(text, y, 0))
    for x in range(1, width):
        output_strings.append(get_diagonal_string(text, 0, x))
    return output_strings


def filter_coordinates(text, coordinates):
    """Remove coordinates that are on the edge of the text"""
    new_coordinates = []
    height = len(text)
    width = len(text[0])
    for coord in coordinates:
        y, x = coord
        if y == 0 or x == 0 or y == height - 1 or x == width - 1:
            pass
        else:
            new_coordinates.append(coord)
    return new_coordinates


def get_corners(text, y, x):
    """Using the y and x coordinates, return the characters at the diagonally adjacent spaces"""
    return (
        text[y - 1][x - 1],
        text[y - 1][x + 1],
        text[y + 1][x + 1],
        text[y + 1][x - 1],
    )


def find_char_coords(text, char):
    """Return all the coordinates that match the character char in the text"""
    coordinates = []
    for y in range(len(text)):
        for x in range(len(text[0])):
            if text[y][x] == char:
                coordinates.append((y, x))
    return coordinates


def test_for_x_mas(corner_values):
    a, b, c, d = corner_values
    left, right = False, False
    if (a == "M" and c == "S") or (a == "S" and c == "M"):
        left = True
    if (b == "M" and d == "S") or (b == "S" and d == "M"):
        right = True
    if left and right:
        return True
    else:
        return False


def get_diagonal_string(text, start_y, start_x):
    """given the starting coordinates at the top left return a sting from the diagonal to the bottom right"""
    height = len(text)
    width = len(text[0])
    diagonal_length = min(height - start_y, width - start_x)
    output_string = ""
    for i in range(diagonal_length):
        output_string += text[start_y + i][start_x + i]
    return output_string


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
