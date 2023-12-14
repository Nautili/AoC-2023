import sys

def roll_north(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'O':
                cur_row = row
                while cur_row > 0 and grid[cur_row - 1][col] == '.':
                    cur_row -= 1
                if cur_row < row:
                    grid[cur_row][col] = 'O'
                    grid[row][col] = '.'
    return grid

def get_load(grid):
    load = 0
    for row_id, row in enumerate(grid):
        for val in row:
            if val == 'O':
                load += len(grid) - row_id
    return load

def rotate(grid):
    new_grid = []
    for col in range(len(grid[0])):
        new_row = []
        for row in reversed(range(len(grid))):
            new_row += grid[row][col]
        new_grid.append(new_row)
    return new_grid

def rotate_n_times(grid, n):
    seen_grids = {}
    found_cycle = False
    i = 0
    while i < n:
        # each cycle ends east
        for _ in range(4):
            grid = roll_north(grid)
            grid = rotate(grid)

        grid_str = ''.join(''.join(row) for row in grid)
        if not found_cycle and grid_str in seen_grids:
            cycle_len = i - seen_grids[grid_str]
            i = n - ((n - i) % cycle_len)
            found_cycle = True
        else:
            seen_grids[grid_str] = i
        i += 1

    return grid
    

def main():
    with open(sys.argv[1]) as f:
        lines = [list(line.strip()) for line in f.readlines()]

    rolled_north = roll_north(lines)
    print(get_load(rolled_north))
    
    spin_cycle = rotate_n_times(lines, 1000000000)
    print(get_load(spin_cycle))

if __name__ == '__main__':
    main()
