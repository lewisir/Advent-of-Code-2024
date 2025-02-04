"""
--- Advent of Code 2024 ---
--- Day 12: Garden Groups ---
https://adventofcode.com/2024/day/12
"""

from time import perf_counter

TEST = False

DAY = "12"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))

TEST1 = ["AAAA", "BBCD", "BBCC", "EEEC"]

TEST2 = ["EEEEE", "EXXXX", "EEEEE", "EXXXX", "EEEEE"]

TEST3 = ["AAAAAA", "AAABBA", "AAABBA", "ABBAAA", "ABBAAA", "AAAAAA"]


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    all_plots = set()
    all_regions = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (y, x) not in all_plots:
                all_regions.append(find_garden_region(data, (y, x)))
                all_plots.update(all_regions[-1])
    fencing = 0
    for region in all_regions:
        fencing += len(region) * calculate_perimeter(region)
    print(f"Part I Fencing required = {fencing}")

    sides = 0
    for region in all_regions:
        sides += len(region) * calculate_sides(region)
    print(f"Part II Fencing with discount = {sides} ")


def calculate_perimeter(region):
    """Given the coordinates of the points in the region, calculate the perimeter"""
    perimeter = 0
    for plot in region:
        perimeter += 4
        for neighbour in region:
            if are_neighbours(plot, neighbour):
                perimeter -= 1
    return perimeter


def calculate_sides(region):
    """Given th coordinates of the points in the region, calculate the sides/corners"""
    sides = 0
    for plot in region:
        sides += count_external_corners(plot, region)
        sides += count_internal_corners(plot, region)
    return sides


def are_neighbours(position1, position2):
    """check whether the two positions are neighbours of one another"""
    y1, x1 = position1
    y2, x2 = position2
    if y1 == y2 and abs(x1 - x2) == 1:
        return True
    elif x1 == x2 and abs(y1 - y2) == 1:
        return True
    else:
        return False


def find_garden_region(garden, plot):
    """Use BFS to find and store all the points of the region"""
    next_plots = [plot]
    region = set()
    plant_type = garden[plot[0]][plot[1]]
    while next_plots:
        current_plot = next_plots.pop()
        region.add(current_plot)
        for neighbour_plot in get_neighbouring_plots(garden, current_plot, plant_type):
            if neighbour_plot not in region:
                next_plots.append(neighbour_plot)
    return region


def get_neighbouring_plots(garden, plot, plant_type):
    """Return the neighbouring plots as long as they are in the garden and of the same plant type"""
    neighbours = []
    for direction in DIRECTIONS:
        neighbour = update_position(plot, direction)
        if (
            neighbour[0] >= 0
            and neighbour[0] < len(garden)
            and neighbour[1] >= 0
            and neighbour[1] < len(garden[0])
            and garden[neighbour[0]][neighbour[1]] == plant_type
        ):
            neighbours.append(neighbour)
    return neighbours


def update_position(position, vector):
    """update the new position based on the vector"""
    return (position[0] + vector[0], position[1] + vector[1])


def count_internal_corners(plot, region):
    """Return the number of internal corners at the plot"""
    corner_count = 0
    y, x = plot
    if (y, x - 1) in region and (y - 1, x) in region and (y - 1, x - 1) not in region:
        corner_count += 1
    if (y - 1, x) in region and (y, x + 1) in region and (y - 1, x + 1) not in region:
        corner_count += 1
    if (y, x + 1) in region and (y + 1, x) in region and (y + 1, x + 1) not in region:
        corner_count += 1
    if (y + 1, x) in region and (y, x - 1) in region and (y + 1, x - 1) not in region:
        corner_count += 1
    return corner_count


def count_external_corners(plot, region):
    """Return the number of external corners at the plot"""
    corner_count = 0
    y, x = plot
    if (y, x - 1) not in region and (y - 1, x) not in region:
        corner_count += 1
    if (y - 1, x) not in region and (y, x + 1) not in region:
        corner_count += 1
    if (y, x + 1) not in region and (y + 1, x) not in region:
        corner_count += 1
    if (y + 1, x) not in region and (y, x - 1) not in region:
        corner_count += 1
    return corner_count


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
