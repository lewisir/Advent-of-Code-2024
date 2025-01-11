"""
--- Advent of Code 2024 ---
--- Day 15: Warehouse Woes ---
https://adventofcode.com/2024/day/15
"""

from time import perf_counter
from pprint import pprint

TEST = False

DAY = "15"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


DIRECTIONS = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    warehouse_map, robot_moves = process_input_data(data)
    position = locate_robot(warehouse_map)
    warehouse_map[position[0]][position[1]] = "."
    for move in robot_moves:
        warehouse_path = extract_warehouse_path(warehouse_map, position, move)
        move_result = check_robot_move(warehouse_path)
        if move_result is not False:
            position = update_position(position, DIRECTIONS[move])
            if move_result > 0:
                box_dest = update_position(position, DIRECTIONS[move], move_result)
                warehouse_map = move_box(warehouse_map, position, box_dest)
    print(f"Part I Sum of all box's GPS = {calculate_gps(warehouse_map)}")


def calculate_gps(warehouse_map):
    """calculate the Goods Positioning System of all the boxes in the map"""
    box_positions = get_box_positions(warehouse_map)
    gps_total = 0
    for position in box_positions:
        gps_total += 100 * position[0] + position[1]
    return gps_total


def get_box_positions(warehouse_map):
    """Return all the positions of all the boxes on the map"""
    box_positions = []
    for y, row in enumerate(warehouse_map):
        for x, value in enumerate(row):
            if value == "O":
                box_positions.append((y, x))
    return box_positions


def move_box(warehouse_map, source, destination):
    """Move the box from the source position to the destination position"""
    warehouse_map[source[0]][source[1]] = "."
    warehouse_map[destination[0]][destination[1]] = "O"
    return warehouse_map


def check_robot_move(warehouse_path):
    """Given the path in the warehouse find whether the robot can move forward"""
    if warehouse_path.count(".") == 0:
        return False
    else:
        return warehouse_path.index(".")


def extract_warehouse_path(warehouse_map, position, direction):
    """Return the list of points from the warehouse map from the position of the robot to the first wall '#'"""
    output_path = []
    position = update_position(position, DIRECTIONS[direction])
    while position_on_map(warehouse_map, position):
        output_path.append(get_value(warehouse_map, position))
        position = update_position(position, DIRECTIONS[direction])
    return output_path


def get_value(warehouse_map, position):
    """Return the value from the warehouse map found at the position"""
    return warehouse_map[position[0]][position[1]]


def position_on_map(warehouse_map, position):
    """Check whether the position is inside the wall"""
    if get_value(warehouse_map, position) == "#":
        return False
    return True


def update_position(position, vector, multiplier=1):
    """Return the new coordinates adding the position and the delta multiplied by the multiplier"""
    delta = multiply_tuple(vector, multiplier)
    return (position[0] + delta[0], position[1] + delta[1])


def multiply_tuple(input_tuple, multiplier):
    """Return the new tuple with each element multiplied by the multiplier"""
    temp_output = []
    for value in input_tuple:
        temp_output.append(value * multiplier)
    return tuple((temp_output))


def locate_robot(warehouse_map):
    """Return the position (y,x) of the robot identified by '@'"""
    for y, row in enumerate(warehouse_map):
        for x, value in enumerate(row):
            if value == "@":
                robot_position = (y, x)
                return robot_position


def process_input_data(data):
    """ "Process the input data to extract the map of the warehouse and the list of robot moves"""
    warehouse_data = []
    robot_moves_data = ""
    for line in data:
        if len(line) == 0:
            continue
        if line[0] == "#":
            warehouse_data.append(line)
        elif line[0] in (">", "<", "^", "v"):
            robot_moves_data += line
        else:
            pass
    warehouse_map = ["_" for _ in range(len(warehouse_data))]
    robot_moves = []
    for index, row in enumerate(warehouse_data):
        warehouse_map[index] = [x for x in row]
    robot_moves = [x for x in robot_moves_data]
    return warehouse_map, robot_moves


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
