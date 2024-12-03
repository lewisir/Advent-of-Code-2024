"""
--- Advent of Code 2024 ---
--- Day 2: Red-Nosed Reports ---
https://adventofcode.com/2024/day/2
"""

from time import perf_counter

TEST = False

DAY = "2"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

MIN = 1
MAX = 3


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    safe_report_count = 0
    for report in process_data(data):
        if check_report(report):
            safe_report_count += 1
    print(f"Part I - Number of Safe Reports - {safe_report_count}")


def check_report(report):
    """Check the sequence of numbers in the report to ensure they adhere to the safe rules"""
    diff = report[0] - report[1]
    sign_check = report[0] - report[1]
    for i in range(1, len(report)):
        diff = report[i - 1] - report[i]
        if not check_in_range(diff):
            return False
        if diff * sign_check < 0:
            return False
    return True


def check_in_range(diff):
    """return False if the difference between the two values is out of range"""
    if abs(diff) < MIN or abs(diff) > MAX:
        return False
    return True


def process_data(data):
    """Extract each line and create a list of integers, returning the list of lists"""
    result_list = []
    for line in data:
        result_list.append(line.split())
        result_list[-1] = convert_entries_to_ints(result_list[-1])
    return result_list


def convert_entries_to_ints(data):
    """Convert each entry in a list to an integer"""
    for i in range(len(data)):
        data[i] = int(data[i])
    return data


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
