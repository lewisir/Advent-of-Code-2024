"""
--- Advent of Code 2024 ---
--- Day 6: Guard Gallivant ---
https://adventofcode.com/2024/day/6
"""

from time import perf_counter
import sys

TEST = False

DAY = "6"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

TURN_RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
MOVE = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    guard_map = process_data(data)
    guard_position = locate_guard(guard_map)
    start_position = guard_position
    guard_facing = "N"
    guard_on_map = True
    guard_points = set(())
    while guard_on_map:
        check_move = check_next_move(guard_map, guard_position, guard_facing)
        if check_move == "forward":
            guard_points.add(guard_position)
            guard_position = add_points(guard_position, MOVE[guard_facing])
        elif check_move == "turn":
            guard_facing = TURN_RIGHT[guard_facing]
        elif check_move == "off_map":
            guard_points.add(guard_position)
            guard_on_map = False
        else:
            pass
    print(f"Part I - Number of Guard Points - {len(guard_points)}")
    guard_points.remove(start_position)
    loop_count = 0
    point_count = 0
    for point in guard_points:
        if check_for_loop(guard_map, start_position, point):
            loop_count += 1
    print(f"Part II - Number of Loops - {loop_count}")


def check_for_loop(guard_map, start_position, point):
    """Count the loops if we add an obstacle at the provided point"""
    guard_map[point[0]][point[1]] = "#"
    guard_position = start_position
    guard_facing = "N"
    guard_on_map = True
    guard_path = set(())
    while guard_on_map:
        check_move = check_next_move(guard_map, guard_position, guard_facing)
        if check_move == "forward":
            guard_path.add((guard_position, guard_facing))
            guard_position = add_points(guard_position, MOVE[guard_facing])
            if (
                guard_position,
                guard_facing,
            ) in guard_path:
                guard_on_map = False
                guard_map[point[0]][point[1]] = "."
                return True
        elif check_move == "turn":
            guard_facing = TURN_RIGHT[guard_facing]
            if (
                guard_position,
                guard_facing,
            ) in guard_path:
                guard_on_map = False
                guard_map[point[0]][point[1]] = "."
                return True
            guard_path.add((guard_position, guard_facing))
        elif check_move == "off_map":
            guard_on_map = False
            guard_map[point[0]][point[1]] = "."
        else:
            pass
    return False


def check_next_move(guard_map, guard_position, guard_facing):
    """Check what happens if the guard moves forwards"""
    new_position = add_points(guard_position, MOVE[guard_facing])
    if not check_on_map(guard_map, new_position):
        return "off_map"
    elif guard_map[new_position[0]][new_position[1]] == "#":
        return "turn"
    else:
        return "forward"


def check_on_map(guard_map, position):
    """Check whether position is on the map"""
    y, x = position
    if y < 0 or y >= len(guard_map):
        return False
    elif x < 0 or x >= len(guard_map[0]):
        return False
    else:
        return True


def add_points(point1, point2):
    """Take the to points and add their corresponding components together"""
    result_point = []
    for component in zip(point1, point2):
        result_point.append(component[0] + component[1])
    return tuple(result_point)


def locate_guard(guard_map):
    """Find the guard and return her location"""
    for y in range(len(guard_map)):
        for x in range(len(guard_map[0])):
            if guard_map[y][x] == "^":
                return (y, x)
    return False


def process_data(data):
    """process the data and return a 2D map"""
    guard_map = []
    for line in data:
        guard_map.append(list(line))
    return guard_map


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
