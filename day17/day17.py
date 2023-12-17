import sys
from queue import PriorityQueue

class State:
    def __init__(self, row, col, prev_loc, straight_len):
        self.row = row
        self.col = col
        self.prev_loc = prev_loc
        self.straight_len = straight_len

    def __lt__(self, other):
        return self.full_tuple() < other.full_tuple()

    def __eq__(self, other):
        return self.full_tuple() == other.full_tuple()

    def __hash__(self):
        return hash(self.full_tuple())

    def full_tuple(self):
        return (self.row, self.col, self.prev_loc.loc_tuple(), self.straight_len) 

    def loc_tuple(self):
        return (self.row, self.col)

def traverse(grid, min_dist, max_dist):
    fake_prev = State(0, 0, None, 0)
    start = State(0, 0, fake_prev, 0)
    rows = len(grid)
    cols = len(grid[0])

    seen = set({start})
    frontier = PriorityQueue()
    frontier.put((0, start))

    while not frontier.empty():
        dist, loc = frontier.get()
        if loc.row == rows - 1 and loc.col == cols - 1 and loc.straight_len >= min_dist:
            return dist

        for d_row, d_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row = loc.row + d_row
            next_col = loc.col + d_col
            if next_row < 0 or next_row >= rows or \
               next_col < 0 or next_col >= cols:
                continue

            # continuing straight
            if loc.prev_loc.row == next_row or loc.prev_loc.col == next_col:
                new_length = loc.straight_len + 1
            # turning too early
            elif loc.straight_len < min_dist:
                continue
            # turning is fine
            else:
                new_length = 1

            next_loc = State(next_row, next_col, loc, new_length)
            if next_loc not in seen and \
               next_loc.loc_tuple() != loc.prev_loc.loc_tuple() and \
               next_loc.straight_len <= max_dist:
                seen.add(next_loc)
                frontier.put((dist + grid[next_row][next_col], next_loc))

def main():
    with open(sys.argv[1]) as f:
        grid = [[int(c) for c in line.strip()] for line in f.readlines()]

    print(traverse(grid, 0, 3))
    print(traverse(grid, 4, 10))

if __name__ == '__main__':
    main()
