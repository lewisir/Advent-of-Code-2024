"""
--- Advent of Code 2024 ---
--- Day 15: Warehouse Woes ---
https://adventofcode.com/2024/day/15
"""

from time import perf_counter

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

    warehouse_map, robot_moves = process_input_data(data)
    exp_wh_map = expand_map(warehouse_map)
    position = locate_robot(exp_wh_map)
    lh_box_points = extract_positions(exp_wh_map, "[")
    rh_box_points = extract_positions(exp_wh_map, "]")
    wall_points = extract_positions(exp_wh_map, "#")
    warehouse_data = (lh_box_points, rh_box_points, wall_points)
    exp_wh_map[position[0]][position[1]] = "."

    for move in robot_moves:
        box_eval = evaluate_box_moves(warehouse_data, position, move, list(()))
        if box_eval is not None:
            position = update_position(position, DIRECTIONS[move])
            if len(box_eval) > 0:
                move_boxes(box_eval, move, lh_box_points, rh_box_points)
                warehouse_data = (lh_box_points, rh_box_points, wall_points)

    gps_score = 0
    for position in lh_box_points:
        gps_score += 100 * position[0] + position[1]
    print(f"Part II Sum of all box's GPS = {gps_score}")


def evaluate_box_moves(warehouse_data, position, move, moving_box_points=set(())):
    """Evaluate whether the move can be made from the position and return the list of box_points if it can
    this is a little inefficient since the moving_box_points can contain duplicate entries
    clean_list() is called to reduce the size of the list
    """
    lh_box_points, rh_box_points, wall_points = warehouse_data
    new_position = update_position(position, DIRECTIONS[move])
    if new_position in wall_points:
        return None
    elif new_position in lh_box_points or new_position in rh_box_points:
        moving_box_points.append(new_position)
        if move in ("^", "v"):
            if new_position in lh_box_points:
                alt_position = update_position(new_position, DIRECTIONS[">"])
            else:
                alt_position = update_position(new_position, DIRECTIONS["<"])
            moving_box_points.append(alt_position)
            box_evaluation = evaluate_box_moves(
                warehouse_data, new_position, move, moving_box_points
            )
            if box_evaluation is not None:
                moving_box_points.extend(box_evaluation)
            else:
                return None
            box_evaluation = evaluate_box_moves(
                warehouse_data, alt_position, move, moving_box_points
            )
            if box_evaluation is not None:
                moving_box_points.extend(box_evaluation)
            else:
                return None
            return clean_list(moving_box_points)
        else:
            box_evaluation = evaluate_box_moves(
                warehouse_data, new_position, move, moving_box_points
            )
            if box_evaluation is not None:
                moving_box_points.extend(box_evaluation)
                return clean_list(moving_box_points)
            else:
                return None
    else:
        return clean_list(moving_box_points)


def move_boxes(moving_boxes, move, lh_box_points, rh_box_points):
    """Update the left and right hand box points with the moved boxes"""
    lh_box_points = update_box_positions(moving_boxes, lh_box_points, move)
    rh_box_points = update_box_positions(moving_boxes, rh_box_points, move)
    return lh_box_points, rh_box_points


def update_box_positions(moving_boxes, box_positions, move):
    """Update the positions of the moving boxes in the list of box positions"""
    for index, box in enumerate(box_positions):
        if box in moving_boxes:
            box_positions[index] = update_position(box, DIRECTIONS[move])
    return box_positions


def calculate_gps(warehouse_map, item="O"):
    """calculate the Goods Positioning System of all the boxes in the map"""
    box_positions = extract_positions(warehouse_map, item)
    gps_total = 0
    for position in box_positions:
        gps_total += 100 * position[0] + position[1]
    return gps_total


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
    return [position[0] + delta[0], position[1] + delta[1]]


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


def extract_positions(warehouse_map, item):
    """return a set of all the positions where the item is found"""
    positions = list(())
    for y, row in enumerate(warehouse_map):
        for x, value in enumerate(row):
            if value == item:
                positions.append([y, x])
    return positions


def expand_map(warehouse_map):
    """Expand the map according to the rules '#' > '##', '.' > '..', 'O' > '[]', '@' > '@.'"""
    new_map = []
    for y, row in enumerate(warehouse_map):
        new_map.append([])
        for x, value in enumerate(row):
            if value == ".":
                new_map[-1].extend([".", "."])
            elif value == "#":
                new_map[-1].extend(["#", "#"])
            elif value == "O":
                new_map[-1].extend(["[", "]"])
            elif value == "@":
                new_map[-1].extend(["@", "."])
    return new_map


def display_map(warehouse_map):
    """Display the map"""
    for row in warehouse_map:
        print("".join(row))


def display_warehouse(warehouse_data):
    """Display the warehouse from the data"""
    lh_box_points, rh_box_points, wall_points = warehouse_data
    warehouse_height, warehouse_width = 0, 0
    for wall_point in wall_points:
        if wall_point[0] > warehouse_height:
            warehouse_height = wall_point[0]
        if wall_point[1] > warehouse_width:
            warehouse_width = wall_point[1]
    warehouse_width += 1
    warehouse_height += 1
    new_warehouse = [
        ["." for i in range(warehouse_width)] for j in range(warehouse_height)
    ]
    for point in lh_box_points:
        y, x = point
        new_warehouse[y][x] = "["
    for point in rh_box_points:
        y, x = point
        new_warehouse[y][x] = "]"
    for point in wall_points:
        y, x = point
        new_warehouse[y][x] = "#"
    display_map(new_warehouse)


def clean_list(input_list):
    """remove duplicates from the input_list"""
    if input_list is None:
        return None
    output_list = []
    for item in input_list:
        if item not in output_list:
            output_list.append(item)
    return output_list


def execute_tests(warehouse_data):
    """Execture defined tests"""
    print(f"TEST [1,3],'<' {evaluate_box_moves(warehouse_data,[1,3],'<',list(()))}")
    print(f"TEST [1,3],'>' {evaluate_box_moves(warehouse_data,[1,3],'>',list(()))}")
    print(f"TEST [1,5],'>' {evaluate_box_moves(warehouse_data,[1,5],'>',list(()))}")
    print(f"TEST [3,8],'<' {evaluate_box_moves(warehouse_data,[3,8],'<',list(()))}")
    print(f"TEST [2,6],'^' {evaluate_box_moves(warehouse_data,[2,6],'^',list(()))}")
    print(f"TEST [2,6],'v' {evaluate_box_moves(warehouse_data,[2,6],'v',list(()))}")

    return None


def process_input_data(data):
    """Process the input data to extract the map of the warehouse and the list of robot moves"""
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
