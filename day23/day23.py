import sys
from collections import deque

class SearchState:
    def __init__(self, cur, prev, dist, edge_dist, prev_node=None):
        self.cur = cur
        self.prev = prev
        self.dist = dist
        self.edge_dist = edge_dist
        self.prev_node = prev_node
    
orth_dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

def build_graph(grid):
    dists = [[0] * len(grid[0])] * len(grid)
    graph = {}
    end_state = SearchState((len(grid) - 2, len(grid[0]) - 2),
                            (len(grid) - 1, len(grid[0]) - 2),
                            1,
                            1,
                            (len(grid) - 1, len(grid[0]) - 2))
    frontier = deque({end_state})

    while frontier:
        cur_state = frontier.popleft()
        cur_row, cur_col = cur_state.cur
        if grid[cur_row][cur_col] == '+':
            if cur_state.cur not in graph:
                graph[cur_state.cur] = {}
            if cur_state.prev_node not in graph:
                graph[cur_state.prev_node] = {}
            graph[cur_state.cur][cur_state.prev_node] = cur_state.edge_dist
            graph[cur_state.prev_node][cur_state.cur] = cur_state.edge_dist
            cur_state.edge_dist = 0
            cur_state.prev_node = cur_state.cur

        for dir in orth_dirs:
            next_row = cur_row + dir[0]
            next_col = cur_col + dir[1]
            if next_row >= 0 and next_row < len(grid) and \
               next_col >= 0 and next_col < len(grid[0]) and \
               cur_state.prev != (next_row, next_col) and \
               (grid[next_row][next_col] == '.' or \
                grid[next_row][next_col] == '+' or \
               (grid[next_row][next_col] == '>' and dir == (0, -1)) or
               (grid[next_row][next_col] == 'v' and dir == (-1, 0))):
                new_dist = max(dists[next_row][next_col], cur_state.dist + 1)
                dists[next_row][next_col] = new_dist
                # this could be optimized by checking that all incoming paths are accounted for
                # but this runs fast enough as is
                frontier.append(SearchState((next_row, next_col),
                                            cur_state.cur,
                                            cur_state.dist + 1,
                                            cur_state.edge_dist + 1,
                                            cur_state.prev_node))
    return dists[0][1], graph

def get_longest_path(graph, cur_node, end, remaining):
    if cur_node == end:
        return 0

    max_dist = 0
    for adj, dist in graph[cur_node].items():
        if adj in remaining:
            remaining.remove(adj)
            max_dist = max(max_dist, get_longest_path(graph, adj, end, remaining) + dist)
            remaining.add(adj)

    return max_dist

def add_crossings(graph):
    for row in range(1, len(graph) - 1):
        for col in range(1, len(graph[0]) - 1):
            if graph[row][col] == '.':
                path_count = 0
                for dir in orth_dirs:
                    if graph[row + dir[0]][col + dir[1]] != '#':
                        path_count += 1
                if path_count > 2:
                    graph[row][col] = '+'
    graph[0][1] = '+'
    graph[len(graph) - 1][len(graph[0]) - 2] = '+'

def print_graph(graph):
    seen = set()
    for s, d_p in graph.items():
        for d, dist in d_p.items():
            if ((s, d)) not in seen:
                print(s, d, dist)
                seen.add((s, d))
                seen.add((d, s))

def main():
    with open(sys.argv[1]) as f:
        grid = [list(line.strip()) for line in f.readlines()]

    add_crossings(grid)

    longest_path, graph = build_graph(grid)
    print_graph(graph)
    print("longest directed path", longest_path)
    print("longest undirected path",
          get_longest_path(graph,
                           (0, 1),
                           (len(grid) - 1, len(grid[0]) - 2),
                           set(graph.keys())))

if __name__ == '__main__':
    main()
