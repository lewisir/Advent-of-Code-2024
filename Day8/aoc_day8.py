"""
--- Advent of Code 2024 ---
--- Day 8: Resonant Collinearity ---
https://adventofcode.com/2024/day/8
"""

from time import perf_counter

TEST = False

DAY = "8"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    max_y = len(data)
    max_x = len(data[0])
    antennas = extract_antenna(data)
    antinodes = set()
    for antenna in antennas.values():
        antenna_pairs = loop_through_pairs(antenna)
        for pair in antenna_pairs:
            an1, an2 = calculate_antinodes(pair[0], pair[1])
            antinodes.add(an1)
            antinodes.add(an2)

    count = 0
    for antinode in antinodes:
        if check_in_range(max_y, max_x, antinode):
            count += 1
    print(f"Part I - Number of Antinodes {count}")

    part_ii_antinodes = set()
    for antenna in antennas.values():
        antenna_pairs = loop_through_pairs(antenna)
        for pair in antenna_pairs:
            part_ii_antinodes.update(
                calculate_extended_antinodes(pair[0], pair[1], max_y, max_x)
            )
    print(f"Part II - Number of antinodes {len(part_ii_antinodes)}")


def loop_through_pairs(pairs):
    """return a list of the pairs of points"""
    pairs_of_pairs = []
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pairs_of_pairs.append((pairs[i], pairs[j]))
    return pairs_of_pairs


def extract_antenna(data):
    """Find all the antennas in the map and return a dictionary of all the antenna points"""
    antennas = {}
    y = 0
    for line in data:
        x = 0
        for char in line:
            if char != ".":
                if antennas.get(char):
                    antennas[char].append((y, x))
                else:
                    antennas[char] = [(y, x)]
            x += 1
        y += 1
    return antennas


def calculate_antinodes(point1, point2):
    """Given the two points return the antinodes"""
    y1, x1 = point1
    y2, x2 = point2
    antinode1 = (2 * y1 - y2, 2 * x1 - x2)
    antinode2 = (2 * y2 - y1, 2 * x2 - x1)
    return antinode1, antinode2


def calculate_extended_antinodes(point1, point2, max_y, max_x):
    """Extend the antinodes across the whole map and return the set of antinodes for the pair of points"""
    y1, x1 = point1
    y2, x2 = point2
    extended_antinodes = set()
    fwd_vector = (y1 - y2, x1 - x2)
    bkw_vector = (y2 - y1, x2 - x1)
    antinode = point1
    on_map = True
    while on_map:
        extended_antinodes.add(antinode)
        antinode = add_points(antinode, fwd_vector)
        on_map = check_in_range(max_y, max_x, antinode)
    antinode = point2
    on_map = True
    while on_map:
        extended_antinodes.add(antinode)
        antinode = add_points(antinode, bkw_vector)
        on_map = check_in_range(max_y, max_x, antinode)
    return extended_antinodes


def add_points(point, vector):
    """Return the new point having been updated by the vector"""
    y, x = point
    vy, vx = vector
    return (y + vy, x + vx)


def check_in_range(max_y, max_x, point):
    """Retrun True if the point is in the range"""
    y, x = point
    if y < 0 or y >= max_y:
        return False
    if x < 0 or x >= max_x:
        return False
    return True


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
