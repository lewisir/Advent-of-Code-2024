"""
--- Advent of Code 2024 ---
--- Day 9: Disk Fragmenter ---
https://adventofcode.com/2024/day/9
"""

from time import perf_counter

TEST = True

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
    disk_blocks = make_disk_blocks(data[0])
    disk_blocks = defrag(disk_blocks)
    print(f"Part I Checksum = {calcualate_checksum(disk_blocks)}")

    disk_blocks = make_disk_blocks(data[0])
    file_blocks = get_file_blocks(data[0])
    free_blocks = get_free_blocks(data[0])
    disk_blocks = defrag_by_file(file_blocks, free_blocks, disk_blocks)
    
    print(f"Part II Checksum = {calcualate_checksum(disk_blocks)}")


def calcualate_checksum(disk_blocks):
    """Return the calcualated checksum"""
    checksum = 0
    for index,value in enumerate(disk_blocks):
        if type(value) is int:
            checksum += index*value
    return checksum


def defrag_by_file(file_blocks,free_blocks,disk_blocks):
    """defrag the disk by moving whole files"""
    for file_id in range(len(file_blocks)-1,0,-1):
        file_length = file_blocks[file_id][1]
        free_space_position = find_free_space(free_blocks, file_length)
        if free_space_position and free_space_position < file_blocks[file_id][0]:
            free_blocks,disk_blocks = move_file(file_id,file_blocks[file_id][0], file_blocks[file_id][1], free_space_position, free_blocks, disk_blocks)
    return disk_blocks

def move_file(file_id, file_position, file_size, destination, free_blocks, disk_blocks):
    """Move the file from to the new position"""
    for i in range(file_size):
        disk_blocks[destination+i] = file_id
        disk_blocks[file_position+i] = '.'
    for index,space in enumerate(free_blocks):
        if space[0] == destination:
            free_blocks[index] = (destination+file_size,space[1]-file_size)
    return free_blocks,disk_blocks



def find_free_space(free_blocks, block_length):
    """return the position of the first free block what is at least as big as the block_length. Else return None"""
    for space in free_blocks:
        if space[1] >= block_length:
            return space[0]
    return None

def defrag(disk_blocks):
    """Defragment the disk moving file ids from the end to the first free space"""
    first_free_block = disk_blocks.index('.')
    last_file_block = find_last_file_block(disk_blocks)
    while first_free_block < last_file_block:
        disk_blocks[first_free_block] = disk_blocks[last_file_block]
        disk_blocks[last_file_block] = '.'
        first_free_block = disk_blocks.index('.')
        last_file_block = find_last_file_block(disk_blocks)
        # print(f"{100*first_free_block/last_file_block}% Complete")
    return disk_blocks

def find_last_file_block(disk_blocks):
    """return the positin of the last file block"""
    for i in range(len(disk_blocks)-1,0,-1):
        if type(disk_blocks[i]) is int:
            return i

def make_disk_blocks(disk_map):
    """produce a list of the disk blocks from the disk map showing file IDs and free space"""
    disk_blocks = []
    file_id = 0
    for digit in range(len(disk_map)):
        if digit % 2 == 0:
            for blocks in range(int(disk_map[digit])):
                disk_blocks.append(file_id)
            file_id += 1
        else:
            for blocks in range(int(disk_map[digit])):
                disk_blocks.append('.')
    return disk_blocks


def get_file_blocks(disk_map):
    """return a dictionary of file IDs and their block locations"""
    file_blocks = {}
    file_id = 0
    position = 0
    for digit in range(len(disk_map)):
        if digit % 2 == 0:
            file_blocks[file_id] = (position,int(disk_map[digit]))
            file_id += 1
        position += int(disk_map[digit])
    return file_blocks

def get_free_blocks(disk_map):
    """return a list of the free blocks"""
    free_blocks = []
    position = 0
    for digit in range(len(disk_map)):
        if digit % 2 == 1:
            free_blocks.append((position,int(disk_map[digit])))
        position += int(disk_map[digit])
    return free_blocks


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
