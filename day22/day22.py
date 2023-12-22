import sys
from collections import deque

class Node:
    def __init__(self, block):
        self.block = block
        self.prev = []
        self.next = []

def over(t, b):
    if t[0][0] > b[1][0] or b[0][0] > t[1][0] or \
       t[0][1] > b[1][1] or b[0][1] > t[1][1]:
        return False
    return True

def build_dependency_graph(blocks):
    z_sorted_blocks = sorted(blocks, key = lambda block: (block[0][2], block[1][2]))
    dropped_blocks = []
    for block in z_sorted_blocks:
        new_node = Node(block)
        covered_blocks = [dropped for dropped in dropped_blocks
                          if over(new_node.block, dropped.block)]
        max_z = max([dropped.block[1][2] for dropped in covered_blocks] + [0])

        new_block = new_node.block
        new_block[1] = (new_block[1][0],
                        new_block[1][1],
                        new_node.block[1][2] - new_node.block[0][2] + max_z + 1)
        new_block[0] = (new_block[0][0],
                        new_block[0][1],
                        max_z + 1)

        for covered in covered_blocks:
            if covered.block[1][2] == max_z:
                new_node.prev.append(covered)
                covered.next.append(new_node)
        dropped_blocks.append(new_node)

    return dropped_blocks

def get_cut_nodes_helper(node, cut_nodes, seen_nodes):
    seen_nodes.add(node)
    if len(node.prev) == 1:
        for prev in node.prev:
            cut_nodes.add(prev)
    for prev in node.prev:
        if prev not in seen_nodes:
            get_cut_nodes_helper(prev, cut_nodes, seen_nodes)

def get_cut_nodes(graph):
    seen_nodes = set()
    cut_nodes = set()
    for node in graph:
        get_cut_nodes_helper(node, cut_nodes, seen_nodes)
    return cut_nodes

def get_fallen(cut_nodes):
    total_fallen = 0
    for node in cut_nodes:
        seen = {node}
        frontier = deque()
        for next in node.next:
            if all(prev in seen for prev in next.prev):
                frontier.append(next)
                seen.add(next)

        # recursively get fallen from initial node set
        while frontier:
            cur_node = frontier.popleft()
            total_fallen += 1
            for next in cur_node.next:
                if next not in seen and all(prev in seen for prev in next.prev):
                    frontier.append(next)
                    seen.add(next)
    return total_fallen

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]
    blocks = []
    for line in lines:
        block = []
        for coord in line.split('~'):
            block.append(tuple(int(val) for val in coord.split(',')))
        blocks.append(block)

    graph = build_dependency_graph(blocks)
    cut_nodes = get_cut_nodes(graph)
    print("cut nodes:", len(lines) - len(cut_nodes))
    print("fallen:", get_fallen(cut_nodes))

if __name__ == '__main__':
    main()
