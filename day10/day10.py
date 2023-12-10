import sys
from collections import deque

adj_map = {
   '|': [(-1, 0), (1, 0)], 
   '-': [(0, -1), (0, 1)], 
   'L': [(-1, 0), (0, 1)], 
   'J': [(-1, 0), (0, -1)], 
   '7': [(1, 0), (0, -1)], 
   'F': [(1, 0), (0, 1)], 
   '.': [],
   'S': [],
}

def get_start(map):
    for row_idx, row in enumerate(map):
        for col_idx, val in enumerate(row):
            if val == 'S':
                return ((row_idx, col_idx))

def get_farthest_point(map):
    start = get_start(map)
    seen = set(start)
    frontier = deque()

    # find valid adjacent pipes
    orth_dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    start_dirs = set()
    for dir in orth_dirs:
        adj_dir = ((dir[0] + start[0], dir[1] + start[1]))
        next_pipe = map[adj_dir[0]][adj_dir[1]]
        for adj_diff in adj_map[next_pipe]:
            if dir[0] + adj_diff[0] == 0 and dir[1] + adj_diff[1] == 0:
                frontier.append((adj_dir, 1))
                seen.add(adj_dir)
                start_dirs.add((dir))

    # replace the start for part 2
    for pipe, dirs in adj_map.items():
        if set(dirs) == start_dirs:
            map[start[0]] = map[start[0]].replace("S", pipe)

    longest_path = 0
    while frontier:
        (cur_row, cur_col), depth = frontier.popleft()
        longest_path = max(longest_path, depth)
        for off_row, off_col in adj_map[map[cur_row][cur_col]]:
            next_pos = ((cur_row + off_row, cur_col + off_col))
            if next_pos not in seen:
                frontier.append((next_pos, depth + 1)) 
                seen.add(next_pos)

    return longest_path, seen

def count_inside_diagonal(map, seen):
    inside_total = 0
    for diagonal in range(len(map) + len(map[0]) - 2):
        is_inside = False
        for row in range(diagonal + 1):
            col = diagonal - row
            if (row, col) in seen:
                if map[row][col] not in "FJ":
                    is_inside = not is_inside
            elif is_inside:
                inside_total += 1
    return inside_total


def main():
    with open(sys.argv[1]) as f:
        map = [line.strip() for line in f.readlines()]

    # part 1
    longest_path, seen = get_farthest_point(map)
    print(longest_path)

    # part 2
    print(count_inside_diagonal(map, seen))

if __name__ == '__main__':
    main()
