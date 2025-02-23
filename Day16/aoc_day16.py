"""
--- Advent of Code 2024 ---
--- Day 16: Reindeer Maze ---
https://adventofcode.com/2024/day/16
"""

from time import perf_counter
from pprint import pprint
import heapq

TEST = False

DAY = "16"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test_II.txt"

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
    maze_path_result = maze_search(maze, start_position, "E", TURN_COST)
    least_cost = maze_path_result[end_position][0]
    print(f"Part I - Lowest Score = {least_cost}")
    # path_points = recursive_path_search(
    #    maze, start_position, end_position, [], "E", least_cost, TURN_COST, 0, set(())
    # )
    new_maze_spf_data = maze_spf(maze, start_position, "E")
    # pprint(new_maze_spf_data)
    path_points = extract_all_points_on_shortest_paths(
        new_maze_spf_data, start_position, end_position, least_cost, set(())
    )
    path_points.add(start_position)
    # print(path_points)
    print(f"Part II Total Points {len(path_points)}")
    # display_maze(maze, path_points, "O")


def maze_search(maze, start_position, direction, turn_cost):
    """Use SPF to find the lowest cost from start to goal"""
    next_nodes = []
    heapq.heappush(next_nodes, (0, (start_position, direction)))
    cost_so_far = {start_position: 0}
    path_data = {start_position: (0, None)}
    while next_nodes:
        new_neighbour = heapq.heappop(next_nodes)[1]
        current, direction = new_neighbour
        for next in get_neighbours(maze, current, direction, turn_cost):
            new_cost = cost_so_far[current] + next[2]
            if next[0] not in cost_so_far or new_cost < cost_so_far[next[0]]:
                cost_so_far[next[0]] = new_cost
                path_data[next[0]] = (new_cost, current)
                heapq.heappush(next_nodes, (new_cost, (next[0], next[1])))
    return path_data


def maze_spf(maze, start_position, direction):
    """USe SPF to find the shortest path to each (point,direction) tuple in the maze"""
    candidate_nodes = []
    heapq.heappush(candidate_nodes, (0, (start_position, direction)))
    spf_data = {(start_position, direction): (0, None)}
    while candidate_nodes:
        new_node = heapq.heappop(candidate_nodes)[1]
        current, direction = new_node
        for next in get_neighbours(maze, current, direction):
            new_cost = spf_data[new_node][0] + next[2]
            if (next[0], next[1]) not in spf_data or new_cost < spf_data[
                (next[0], next[1])
            ][0]:
                spf_data[(next[0], next[1])] = (new_cost, current)
                heapq.heappush(candidate_nodes, (new_cost, (next[0], next[1])))
    return spf_data


def extract_shortest_path(path_data, start, end):
    """Return the list of points used to get from the start to the end"""
    point = end
    path = [point]
    while point != start:
        point = path_data[point][1]
        path.append(point)
    path.reverse()
    return path


def extract_all_points_on_shortest_paths(spf_data, start, point, cost, all_path_points):
    """Extract all the points in the shortest paths"""
    if point == start:
        return all_path_points
    else:
        temp_key_list = []
        for point_dir in spf_data.keys():
            if point_dir[0] == point:
                temp_key_list.append(point_dir)
        for key in temp_key_list:
            if spf_data[key][0] <= cost:
                all_path_points.add(point)
                old_cost = cost
                cost, point = spf_data[key]
                all_path_points.update(
                    extract_all_points_on_shortest_paths(
                        spf_data, start, point, cost, all_path_points
                    )
                )
                cost = old_cost
    return all_path_points


def recursive_path_search(
    maze,
    position,
    target,
    path_so_far,
    direction,
    cost_limit,
    turn_cost,
    cost=0,
    all_paths_points=set(()),
):
    """Find all paths to the target"""
    path_so_far.append(position)
    if position == target:
        all_paths_points.update(path_so_far)
    else:
        for next_point_data in get_neighbours(maze, position, direction, turn_cost):
            next_point, direction, delta_cost = next_point_data
            if next_point not in path_so_far:
                cost += delta_cost
                if cost <= cost_limit:
                    recursive_path_search(
                        maze,
                        next_point,
                        target,
                        path_so_far,
                        direction,
                        cost_limit,
                        turn_cost,
                        cost,
                        all_paths_points,
                    )
                    path_so_far.pop()
                cost -= delta_cost
    return all_paths_points


def get_neighbours(maze, position, direction, turn_cost=TURN_COST):
    neighbours = []
    forward_neighbour = update_position(position, DIRECTIONS[direction])
    if (
        check_in_maze(maze, forward_neighbour)
        and get_maze_item(maze, forward_neighbour) != "#"
    ):
        neighbours.append((forward_neighbour, direction, FWD_COST))
    left_neighbour = update_position(position, DIRECTIONS[TURN[direction]["L"]])
    if (
        check_in_maze(maze, left_neighbour)
        and get_maze_item(maze, left_neighbour) != "#"
    ):
        neighbours.append((left_neighbour, TURN[direction]["L"], turn_cost + FWD_COST))
    right_neighbour = update_position(position, DIRECTIONS[TURN[direction]["R"]])
    if (
        check_in_maze(maze, right_neighbour)
        and get_maze_item(maze, right_neighbour) != "#"
    ):
        neighbours.append((right_neighbour, TURN[direction]["R"], turn_cost + FWD_COST))
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


def update_position(position, direction):
    """Return the new position having moved in the direction"""
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


def display_maze(maze, overlay, character):
    """print out the maze but update the positions in overlay with the character"""
    temp_maze = maze.copy()
    for point in overlay:
        y, x = point
        temp_maze[y][x] = character
    output_map = ["".join(x) for x in temp_maze]
    for line in output_map:
        print(line)


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
