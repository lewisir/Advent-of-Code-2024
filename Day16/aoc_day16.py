"""
--- Advent of Code 2024 ---
--- Day 16: Reindeer Maze ---
https://adventofcode.com/2024/day/16
"""

from time import perf_counter
from pprint import pprint
import heapq

TEST = True

DAY = "16"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
TURN = {
    "N": {"R": "E", "L": "W"},
    "S": {"R": "W", "L": "E"},
    "E": {"R": "S", "L": "N"},
    "W": {"R": "N", "L": "S"},
}
FWD_COST = 1
TURN_COST = 1000


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    maze = process_data(data)
    start_position = locate_in_maze(maze, "S")[0]
    end_position = locate_in_maze(maze, "E")[0]
    maze_path_result = maze_search(maze, start_position, "E", end_position)
    print(f"Part I - Lowest Score = {maze_path_result[end_position]}")


def maze_search(maze, start_position, direction, goal):
    """Use SPF to find the shortest path from start to goal"""
    next_nodes = []
    heapq.heappush(next_nodes, (0, (start_position, direction)))
    cost_so_far = {start_position: 0}
    while next_nodes:
        new_neighbour = heapq.heappop(next_nodes)[1]
        current = new_neighbour[0]
        direction = new_neighbour[1]
        if current == goal:
            break
        for next in get_current_neighbours(maze, current, direction):
            new_cost = cost_so_far[current] + next[2]
            if next[0] not in cost_so_far or new_cost < cost_so_far[next[0]]:
                cost_so_far[next[0]] = new_cost
                heapq.heappush(next_nodes, (new_cost, (next[0], next[1])))
    return cost_so_far


def get_current_neighbours(maze, position, direction):
    """Return a list of possible valid neighbouring points"""
    neighbours = []
    fwd_nghbr = update_position(position, DIRECTIONS[direction])
    if check_in_maze(maze, fwd_nghbr):
        if get_maze_item(maze, fwd_nghbr) != "#":
            neighbours.append((fwd_nghbr, direction, FWD_COST))
    lft_nghbr = update_position(position, DIRECTIONS[TURN[direction]["L"]])
    if check_in_maze(maze, lft_nghbr):
        if get_maze_item(maze, lft_nghbr) != "#":
            neighbours.append((lft_nghbr, TURN[direction]["L"], TURN_COST + FWD_COST))
    rght_nghbr = update_position(position, DIRECTIONS[TURN[direction]["R"]])
    if check_in_maze(maze, rght_nghbr):
        if get_maze_item(maze, rght_nghbr) != "#":
            neighbours.append((rght_nghbr, TURN[direction]["R"], TURN_COST + FWD_COST))
    opposite_dir = TURN[TURN[direction]["R"]]["R"]
    bkwd_nghbr = update_position(position, DIRECTIONS[opposite_dir])
    if check_in_maze(maze, bkwd_nghbr):
        if get_maze_item(maze, bkwd_nghbr) != "#":
            neighbours.append((bkwd_nghbr, opposite_dir, 2 * TURN_COST + FWD_COST))
    return neighbours


def check_in_maze(maze, position):
    """Check with the position is within the maze boundary"""
    if (
        position[0] >= 0
        and position[0] < len(maze)
        and position[1] >= 0
        and position[1] < len(maze[0])
    ):
        return True
    return False


def check_turn(maze, position, direction, turn):
    """Check whether it's possible to turn"""
    new_direction = TURN[direction][turn]
    new_position = update_position(position, DIRECTIONS[new_direction])
    item = get_maze_item(maze, new_position)
    if item == "#":
        return False
    else:
        return True


def update_position(position, direction):
    """Return the new position having moved in the direction"""
    output_position = ["y", "x"]
    output_position[0] = position[0] + direction[0]
    output_position[1] = position[1] + direction[1]
    return (position[0] + direction[0], position[1] + direction[1])


def get_maze_item(maze, position):
    """return the item at the position in the maze"""
    y, x = position
    return maze[y][x]


def locate_in_maze(maze, item):
    """Return the positions of the item in the maze"""
    positions = []
    for y, row in enumerate(maze):
        for x, value in enumerate(row):
            if value == item:
                positions.append((y, x))
    return positions


def process_data(data):
    """process the data to convert to a list of lists"""
    maze = ["_" for _ in range(len(data))]
    for index, row in enumerate(data):
        maze[index] = [x for x in row]
    return maze


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
