"""
--- Advent of Code 2024 ---
--- Day 13: Claw Contraption ---
https://adventofcode.com/2024/day/13
"""

from time import perf_counter

TEST = False

DAY = "13"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    claw_machine_data = process_data(data)
    token_count = 0
    for machine in claw_machine_data:
        result = sim_equ(machine)
        if result is not None:
            a, b = result
            token_count += 3 * a + b
    print(f"Part I Tokens = {token_count}")


def sim_equ(input_variables):
    """solve the equations returning a and b where:
    a * but_a_x + b * but_b_x = target_x
    a * but_a_y + b * but_b_y = target_y
    if there is no solution return None
    """
    target_x, target_y, but_a_x, but_a_y, but_b_x, but_b_y = input_variables
    b = int(
        (target_x * but_a_y - but_a_x * target_y)
        / (but_b_x * but_a_y - but_a_x * but_b_y)
    )
    a = int(
        (target_y * but_b_x - but_b_y * target_x)
        / (but_a_y * but_b_x - but_b_y * but_a_x)
    )
    x_test = a * but_a_x + b * but_b_x
    y_test = a * but_a_y + b * but_b_y
    if a < 0 or b < 0 or a > 100 or b > 100 or x_test != target_x or y_test != target_y:
        return None
    else:
        return a, b


def process_data(data):
    """Process the data to return the claw machine information; location of prize and function of buttons"""
    claw_machine_data = []
    for line in data:
        if line.find("Button A") == 0:
            claw_machine_data.append([])
            but_a_x, but_a_y = extract_x_y_data(line)
        elif line.find("Button B") == 0:
            but_b_x, but_b_y = extract_x_y_data(line)
        elif line.find("Prize") == 0:
            target_x, target_y = extract_x_y_data(line)
            claw_machine_data[-1] = (
                target_x,
                target_y,
                but_a_x,
                but_a_y,
                but_b_x,
                but_b_y,
            )
        else:
            pass
    return claw_machine_data


def extract_x_y_data(data_line):
    """return the X and Y changes made by the button"""
    x = int(data_line.split()[-2][2:-1])
    y = int(data_line.split()[-1][2:])
    return x, y


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
