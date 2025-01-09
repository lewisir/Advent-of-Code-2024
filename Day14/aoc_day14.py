"""
--- Advent of Code 2024 ---
--- Day 14: Restroom Redoubt ---
https://adventofcode.com/2024/day/14
"""

from time import perf_counter

TEST = False

DAY = "14"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

WIDTH = 101
HEIGHT = 103
TIME = 100


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    robot_data = process_data(data)
    final_positions = []
    for robot in robot_data:
        position = (robot[0], robot[1])
        velocity = (robot[2], robot[3])
        final_positions.append(wrap_coordinates(move_robot(position, velocity, TIME)))
    quadrant_counts = count_robots_by_quadrant(final_positions)
    safety_factor = (
        quadrant_counts[0]
        * quadrant_counts[1]
        * quadrant_counts[2]
        * quadrant_counts[3]
    )
    print(f"Part I Safty factor = {safety_factor}")


def count_robots_by_quadrant(robot_positions):
    quadrant_1_count, quadrant_2_count, quadrant_3_count, quadrant_4_count = 0, 0, 0, 0
    for robot in robot_positions:
        x, y = robot[0], robot[1]
        if x < WIDTH // 2 and y < HEIGHT // 2:
            quadrant_1_count += 1
        elif x > WIDTH // 2 and y < HEIGHT // 2:
            quadrant_2_count += 1
        elif x < WIDTH // 2 and y > HEIGHT // 2:
            quadrant_3_count += 1
        elif x > WIDTH // 2 and y > HEIGHT // 2:
            quadrant_4_count += 1
    return quadrant_1_count, quadrant_2_count, quadrant_3_count, quadrant_4_count


def move_robot(position, velocity, time):
    """update the robot's position returning the new position"""
    start_x, start_y = position
    vel_x, vel_y = velocity
    final_x = start_x + vel_x * time
    final_y = start_y + vel_y * time
    return final_x, final_y


def wrap_coordinates(position):
    """return new coordinates based on the positions wrapping around the map"""
    x, y = position
    new_x = x % WIDTH
    new_y = y % HEIGHT
    return new_x, new_y


def process_data(data):
    """Process the data returning a list of the robots, their positions and velocities"""
    robot_data = []
    for line in data:
        position = line.split()[0][2:].split(",")
        velocity = line.split()[1][2:].split(",")
        robot_data.append(
            (int(position[0]), int(position[1]), int(velocity[0]), int(velocity[1]))
        )
    return robot_data


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
