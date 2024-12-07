"""
--- Advent of Code 2024 ---
--- Day 5: Print Queue ---
https://adventofcode.com/2024/day/5
"""

from time import perf_counter

TEST = False

DAY = "5"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    order_rules, page_sequences = process_input_data(data)
    page_number_sum = 0
    for sequence in page_sequences:
        if check_valid_sequence(sequence, order_rules):
            page_number_sum += int(sequence[len(sequence) // 2])
    print(f"Prt I - Middle Page Sum - {page_number_sum}")


def check_valid_sequence(sequence, order_rules):
    """Return True is  the sequence of page numbers adheres to the order rules"""
    for index, page in enumerate(sequence):
        if index == len(sequence) - 1:
            return True
        for scd_idx, next_page in enumerate(sequence[index + 1 :]):
            if scd_idx == len(sequence[index + 1 :]) - 1:
                pass
            if next_page not in order_rules.keys():
                return False
            elif next_page not in order_rules[page]:
                return False
            else:
                pass
    return True


def process_input_data(data):
    """extract the data from the input"""
    order_rules = {}
    page_sequences = []
    for line in data:
        if line.count("|") > 0:
            order_rules = update_page_order_rules(line, order_rules)
        elif line.count(",") > 0:
            page_sequences.append(line.split(","))
        else:
            pass
    return order_rules, page_sequences


def update_page_order_rules(rule, order_rules):
    """Update the order rules with the new rule"""
    key, value = rule.split("|")
    if key not in order_rules.keys():
        order_rules[key] = [value]
    else:
        order_rules[key].append(value)
    return order_rules


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
