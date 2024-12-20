"""
--- Advent of Code 2024 ---
--- Day 7: Bridge Repair ---
https://adventofcode.com/2024/day/7
"""

from time import perf_counter

TEST = False

DAY = "7"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    calibration_data = process_data(data)
    result_sum = 0
    for equation in calibration_data:
        target, sequence = equation
        if perm_calculation(target, sequence):
            result_sum += target
    print(f"Part I Result Sum {result_sum}")


def perm_calculation(target, sequence):
    """Output all of the possible addition and multiplications of the sequence"""
    permutations = 2 ** (len(sequence) - 1)
    for perm in range(permutations):
        calc_result = sequence[0]
        for bit in range(len(sequence) - 1):
            if 2**bit & perm == 0:
                calc_result += sequence[bit + 1]
            elif 2**bit & perm != 0:
                calc_result *= sequence[bit + 1]
            if calc_result > target:
                continue
        if calc_result == target:
            return True
    return False


def process_data(data):
    "Process the input data line by line"
    result_list = []
    for line in data:
        result_list.append(process_line(line))
    return result_list


def process_line(line):
    """Process the line to return the result and the sequence of integers"""
    temp = line.split(":")
    result = int(temp[0])
    sequence = temp[1].split()
    seq = [int(x) for x in sequence]
    return result, seq


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
