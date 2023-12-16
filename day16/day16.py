import sys
from collections import deque

def parse_mirrors(grid):
    mirrors = {}
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val != '.':
                mirrors[(i, j)] = val
    return mirrors

def add_beam(seen, frontier, beam, rows, cols):
    row, col, _, _ = beam
    if row < 0 or col < 0 or row >= rows or col >= cols or beam in seen:
        return
    seen.add(beam)
    frontier.append(beam)

def get_energy(grid, start):
    mirrors = parse_mirrors(grid)
    rows = len(grid)
    cols = len(grid[0])

    seen = {start}
    frontier = deque({start})

    while frontier:
        row, col, d_row, d_col = frontier.popleft()

        cur_mirror = mirrors.get((row, col))
        cur_beam = None
        if not cur_mirror:
            cur_beam = (row + d_row, col + d_col, d_row, d_col)
        elif cur_mirror == '/':
            cur_beam = (row - d_col, col - d_row, -d_col, -d_row)
        elif cur_mirror == '\\':
            cur_beam = (row + d_col, col + d_row, d_col, d_row)
        elif cur_mirror == '|':
            if d_col == 0:
                cur_beam = (row + d_row, col, d_row, d_col)
            else:
                add_beam(seen, frontier, (row - 1, col, -1, 0), rows, cols)
                cur_beam = (row + 1, col, 1, 0)
        elif cur_mirror == '-':
            if d_row == 0:
                cur_beam = (row, col + d_col, d_row, d_col)
            else:
                add_beam(seen, frontier, (row, col - 1, 0, -1), rows, cols)
                cur_beam = (row, col + 1, 0, 1)
        add_beam(seen, frontier, cur_beam, rows, cols)

    return len(set((row, col) for row, col, _, _ in seen))

def get_max_energy(grid):
    rows = len(grid)
    cols = len(grid[0])
    max_energy = 0
    for row in range(rows):
        max_energy = max(max_energy, get_energy(grid, (row, 0, 0, 1)))
        max_energy = max(max_energy, get_energy(grid, (row, cols - 1, 0, -1)))
    for col in range(cols):
        max_energy = max(max_energy, get_energy(grid, (0, col, 1, 0)))
        max_energy = max(max_energy, get_energy(grid, (rows - 1, col, -1, 0)))

    return max_energy

def main():
    with open(sys.argv[1]) as f:
        grid = [line.strip() for line in f.readlines()]

    print(get_energy(grid, (0, 0, 0, 1)))
    print(get_max_energy(grid))

if __name__ == '__main__':
    main()
