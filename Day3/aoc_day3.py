"""
--- Advent of Code 2024 ---
--- Day 3: Mull It Over ---
https://adventofcode.com/2024/day/3
"""

from time import perf_counter

TEST = False

DAY = "3"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

DIGITS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
DIGIT_LIMIT = 3


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    input_string = "".join(data)
    sum = 0
    number_pairs = process_string(input_string)
    for pair in number_pairs:
        sum += pair[0] * pair[1]
    print(f"Part I Sum result = {sum}")
    number_pairs = process_string_with_do(input_string)
    sum = 0
    for pair in number_pairs:
        sum += pair[0] * pair[1]
    print(f"Part II Sum result = {sum}")


def process_string(test_string):
    """return the pairs of numbers that are parts of a valid mul() function"""
    number_pairs = []
    temp_list = test_string.split("mul(")
    for i, x in enumerate(temp_list):
        mul_pair = extract_number_pair(x)
        if mul_pair:
            number_pairs.append(mul_pair)
    return number_pairs


def process_string_with_do(test_string):
    """return the pairs of numbers that are parts of a valid mul() function"""
    number_pairs = []
    temp_list = test_string.split("mul(")
    do = True
    for i, x in enumerate(temp_list):
        mul_pair = extract_number_pair(x)
        if mul_pair and do:
            number_pairs.append(mul_pair)
        if x.find("do()") >= 0:
            do = True
        if x.find("don't()") >= 0:
            do = False
    return number_pairs


def extract_number_pair(input_string):
    """extract a valid number pair from the start of the input string"""
    digit_count = 0
    number_count = 0
    num_a, num_b = "", ""
    for char in input_string:
        if digit_count > DIGIT_LIMIT:
            return False
        elif char in DIGITS and digit_count <= DIGIT_LIMIT and number_count == 0:
            num_a += char
            digit_count += 1
            continue
        elif char in DIGITS and digit_count <= DIGIT_LIMIT and number_count == 1:
            num_b += char
            digit_count += 1
            continue
        elif digit_count < 4 and char == "," and number_count == 0:
            number_count = 1
            digit_count = 0
            continue
        elif digit_count < 4 and char == ")" and number_count == 1:
            number_count = 2
            digit_count = 0
            return int(num_a), int(num_b)
        return False
    return False


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
