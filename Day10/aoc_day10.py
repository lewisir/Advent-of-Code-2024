"""
--- Advent of Code 2024 ---
--- Day 10: Hoof It ---
https://adventofcode.com/2024/day/10
"""

from time import perf_counter

TEST = False

DAY = "10"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

TRAILHEAD = 0
END = 9
DIRECTIONS = [(-1,0), (1,0), (0,1), (0,-1)]
TEST1 = ['1190119','1111198','1112117','6543456','7651987','8761111','9871111']
TEST2 = ['1011911','2111811','3111711','4567654','1118113','1119112','1111101']

def main():
    """Main program"""
    data = get_input_data(FILENAME)
    topographic_map = process_data(data)
    trailheads = find_trailheads(topographic_map)
    trail_count = 0
    for trailhead in trailheads:
        new_trails = explore_trail(trailhead,topographic_map,set())
        trail_count += len(new_trails)
    print(f"Part I Trail Count = {trail_count}")

def explore_trail(position, topographic_map, end_points):
    """for the given position explore to find the number of good trails"""
    if topographic_map[position[0]][position[1]] == END:
        end_points.add(position)
        return end_points
    else:
        for direction in DIRECTIONS:
            current_height = topographic_map[position[0]][position[1]]
            new_position = update_position(position,direction)
            if check_position(new_position,topographic_map):
                if topographic_map[new_position[0]][new_position[1]]-current_height == 1:
                    explore_trail(new_position,topographic_map,end_points)
        return end_points

def update_position(position,vector):
    """Add the vector to the position"""
    return(position[0]+vector[0],position[1]+vector[1])

def check_position(position,topographic_map):
    """Check whether the position is on the map"""
    if position[0] < 0 or position[0] >= len(topographic_map):
        return False
    if position[1] < 0 or position[1] >= len(topographic_map[0]):
        return False
    
    return True

def find_trailheads(topographic_map):
    """Return a list of all the positions of a the trailheads"""
    trailheads = []
    for y,row in enumerate(topographic_map):
        for x, value in enumerate(row):
            if value == TRAILHEAD:
                trailheads.append((y,x))
    return trailheads

def process_data(data):
    """Convert data to integers"""
    topographic_map = []
    for line in data:
        topographic_map.append([int(x) for x in line])
    return topographic_map

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
