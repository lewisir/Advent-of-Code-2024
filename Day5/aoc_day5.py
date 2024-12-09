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
    incorrect_sequences = []
    for sequence in page_sequences:
        if check_valid_sequence(sequence, order_rules):
            page_number_sum += int(sequence[len(sequence) // 2])
        else:
            incorrect_sequences.append(sequence)
    print(f"Part I - Middle Page Sum - {page_number_sum}")
    page_number_sum = 0
    for seq in incorrect_sequences:
        ordered_seq = create_ordered_seq(seq, order_rules)
        delta = int(ordered_seq[len(seq) // 2])
        page_number_sum += int(ordered_seq[len(seq) // 2])
    print(f"Part II - Middle Page Sum - {page_number_sum}")


def check_valid_sequence(sequence, order_rules):
    """Return True if the sequence of page numbers adheres to the order rules"""
    for index, page in enumerate(sequence):
        for next_page in sequence[index + 1 :]:
            if next_page not in order_rules[page]:
                return False
    return True


def create_ordered_seq(seq, order_rules):
    """From the provided sequence, order it according to the order rules"""
    # First generate a specific order rules for this sequence (remove the numbers that are not needed from the order rules)
    specific_order_rules = prune_order_rules(seq, order_rules)
    ordered_sequence = order_sequence(specific_order_rules)
    return ordered_sequence


def prune_order_rules(seq, order_rules):
    """return the order rules that only contain the numbers in the sequence"""
    all_values = order_rules.keys()
    specific_rules = {}
    for key in seq:
        specific_rules[key] = order_rules[key].copy()
    for key, rule in specific_rules.items():
        for value in all_values:
            if value in rule and value not in seq:
                rule.remove(value)
    return specific_rules


def update_sequence_order(sequence, complete_correct_sequence):
    """return a corrected sequence"""
    correct_sequence = complete_correct_sequence.copy()
    keep_elements = set(sequence)
    all_elements = set(complete_correct_sequence)
    elements_to_remove = all_elements - keep_elements
    for element in elements_to_remove:
        correct_sequence.remove(element)
    return correct_sequence


def order_sequence(order_rules):
    """Return a list of all elements in order according to the rules"""
    value_len_dict = {}
    value_sequence = ["_" for i in range(len(order_rules))]
    for key in order_rules:
        value_len = len(order_rules[key])
        value_len_dict[key] = value_len
    for key, value in value_len_dict.items():
        value_sequence[value] = key
    return value_sequence


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
    if value not in order_rules.keys():
        order_rules[value] = []
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
