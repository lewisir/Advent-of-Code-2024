"""
--- Advent of Code 2024 ---
--- Day 9: Disk Fragmenter ---
https://adventofcode.com/2024/day/9
"""

from time import perf_counter

TEST = False

DAY = "9"
REAL_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2024/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    small_disk_test = "12345"
    disk_blocks = make_disk_blocks(data[0])
    disk_blocks = defrag(disk_blocks)
    print(f"Part I Checksum = {calcualate_checksum(disk_blocks)}")

def calcualate_checksum(disk_blocks):
    """Return the calcualated checksum"""
    checksum = 0
    for index,value in enumerate(disk_blocks):
        if type(value) is int:
            checksum += index*value
    return checksum

def defrag(disk_blocks):
    """Defragment the disk moving file ids from the end to the first free space"""
    first_free_block = disk_blocks.index('.')
    last_file_block = find_last_file_block(disk_blocks)
    while first_free_block < last_file_block:
        disk_blocks[first_free_block] = disk_blocks[last_file_block]
        disk_blocks[last_file_block] = '.'
        first_free_block = disk_blocks.index('.')
        last_file_block = find_last_file_block(disk_blocks)
        print(f"{100*first_free_block/last_file_block}% Complete")
    return disk_blocks

def find_last_file_block(disk_blocks):
    """return the positin of the last file block"""
    for i in range(len(disk_blocks)-1,0,-1):
        if type(disk_blocks[i]) is int:
            return i


def extract_disk_blocks(disk_map):
    """Given the disk map return a dictionary of the file IDs and their blocks and a list of the free blocks"""
    file_id = 0
    file_blocks = {}
    free_blocks = []
    position = 0
    for digit in range(len(disk_map)):
        if digit % 2 == 0:
            file_blocks[file_id] = (position, int(disk_map[digit]))
            file_id += 1
        else:
            free_blocks.append((position, int(disk_map[digit])))
        position += int(disk_map[digit])
    return file_blocks, free_blocks


def display_disk_from_blocks(file_blocks):
    """Print a representation of the files on the disk from the disk block"""
    output_string = ""
    for file_id in range(len(file_blocks)):
        if file_blocks[file_id][0] > len(output_string):
            output_string += "." * (file_blocks[file_id][0] - len(output_string))
            output_string += str(file_id) * file_blocks[file_id][1]
        else:
            output_string += str(file_id) * file_blocks[file_id][1]
    print(output_string)

def make_disk_blocks(disk_map):
    """produce a list of the disk blocks from the disk map showing file IDs nd free space"""
    disk_blocks = []
    file_id = 0
    position = 0
    for digit in range(len(disk_map)):
        if digit % 2 == 0:
            for blocks in range(int(disk_map[digit])):
                disk_blocks.append(file_id)
            file_id += 1
        else:
            for blocks in range(int(disk_map[digit])):
                disk_blocks.append('.')
    return disk_blocks

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
