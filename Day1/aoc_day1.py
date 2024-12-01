"""
--- Advent of Code 2024 ---
--- Day 1: Historian Hysteria ---
https://adventofcode.com/2024/day/1
"""

from time import perf_counter

TEST = False

DAY = "1"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    location_ids_1, location_ids_2 = process_input_data(data)
    location_ids_1.sort()
    location_ids_2.sort()
    print(
        f"Part I - Sum of location ID differences - {difference_sum(location_ids_1,location_ids_2)}"
    )
    print(
        f"Part II - Sum of Similarity Score - {similarity_score(location_ids_1,location_ids_2)}"
    )


def similarity_score(list_1, list_2):
    """Given two lists of integers, return the sum of the number of times the number in the first list appears in the second list"""
    sum_similarity_score = 0
    for i, x in enumerate(list_1):
        sum_similarity_score += x * list_2.count(x)
    return sum_similarity_score


def difference_sum(list_1, list_2):
    """Given two lists of integers, return the sum of the absolute differences between the elements of the two lists"""
    sum_diff = 0
    for pair in zip(list_1, list_2):
        sum_diff += abs(pair[0] - pair[1])
    return sum_diff


def process_input_data(data):
    """Return two lists from the input data converting strings to integers"""
    location_ids_1, location_ids_2 = [], []
    for line in data:
        location_id_1, location_id_2 = line.split()
        location_ids_1.append(int(location_id_1))
        location_ids_2.append(int(location_id_2))
    return location_ids_1, location_ids_2


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
