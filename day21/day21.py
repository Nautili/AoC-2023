import sys
from copy import deepcopy

def take_step(grid):
    new_grid = deepcopy(grid)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if new_grid[row][col] == -1:
                continue
            
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            new_grid[row][col] = 0
            for dir in dirs:
                cur_row = row + dir[0]
                cur_col = col + dir[1]
                if cur_row >= 0 and cur_row < len(grid) and \
                   cur_col >= 0 and cur_col < len(grid[row]) \
                   and grid[cur_row][cur_col] > 0:
                    new_grid[row][col] = 1
    return new_grid

def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    symbol_map = {'.': 0, 'S': 1, '#': -1}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col] = symbol_map[grid[row][col]]

    for _ in range(64):
        grid = take_step(grid)
    position_count = sum([c for row in grid for c in row if c >= 0])
    print(position_count)


if __name__ == '__main__':
    main()
