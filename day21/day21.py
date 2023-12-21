import sys

class Node:
    def __init__(self, row, col, prev=[]):
        self.row = row
        self.col = col
        self.prev = prev

def take_step(grid, nodes):
    new_nodes = {}
    for node in nodes:
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cur_row = node.row + dir[0]
            cur_col = node.col + dir[1]
            if (cur_row, cur_col) not in node.prev and \
               cur_row >= 0 and cur_row < len(grid) and \
               cur_col >= 0 and cur_col < len(grid[0]) \
               and grid[cur_row][cur_col] != '#':
                if (cur_row, cur_col) not in new_nodes:
                    new_nodes[(cur_row, cur_col)] = Node(cur_row, cur_col)
                new_nodes[(cur_row, cur_col)].prev.append((node.row, node.col))
    return list(new_nodes.values())

def take_n_steps(grid, start, n):
    nodes = [start]
    count1 = 0
    count2 = 1
    for _ in range(n):
        nodes = take_step(grid, nodes)
        count1, count2 = count2, count1 + len(nodes)
    return count2

def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 'S':
                start = Node(r, c)

    print(take_n_steps(grid, start, 64))


if __name__ == '__main__':
    main()
