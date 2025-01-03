"""
--- Advent of Code 2024 ---
--- Day 11: Plutonian Pebbles ---
https://adventofcode.com/2024/day/11
"""

from time import perf_counter

TEST = False

DAY = "11"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

BLINKS = 25

TEST = "0"


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    stone_list = data[0].split()
    for _ in range(BLINKS):
        # print(stone_list)
        stone_list = process_stone_list(stone_list)
    print(f"Part I - Number of stones after {BLINKS} blinks is {len(stone_list)}")


def process_stone_list(stone_list):
    """Process each stone in the stone list and return a new updated stone list"""
    new_stone_list = []
    for position, stone in enumerate(stone_list):
        if int(stone) == 0:
            new_stone_list.append("1")
        elif len(stone) % 2 == 0:
            left_half, right_half = split_stone(stone)
            new_stone_list.append(left_half)
            new_stone_list.append(right_half)
        else:
            new_stone_list.append(str(int(stone) * 2024))
    return new_stone_list


def split_stone(stone):
    """Split the stone in to parts, left and right and remove leading zeros"""
    left_half = stone[: len(stone) // 2]
    right_half = stone[len(stone) // 2 :]
    left_half = remove_leading_zeros(left_half)
    right_half = remove_leading_zeros(right_half)
    return left_half, right_half


def remove_leading_zeros(text_number):
    """remove leading zeros from the text number"""
    return str(int(text_number))


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
