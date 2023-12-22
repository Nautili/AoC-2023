import sys

class Node:
    def __init__(self, block):
        self.block = block
        self.prev = []
        self.next = []

def over(t, b):
    if t[0][0] > b[1][0] or b[0][0] > t[1][0] or \
       t[0][1] > b[1][1] or b[0][1] > t[1][1] or \
       t[0][2] <= b[1][2]:
        return False
    return True

# returns whether top_node was updated
def add_on_top(new_node, top_node):
    if over(new_node.block, top_node.block):
        top_node.next.append(new_node)
        new_node.prev.append(top_node)
        return True
    else:
        for node in top_node.prev:
            add_on_top(new_node, node)
    return False

def build_dependency_graph(blocks):
    z_sorted_blocks = sorted(blocks, key = lambda block: block[0][2])
    top_nodes = []
    for i, block in enumerate(z_sorted_blocks):
        print(i)
        new_node = Node(block)
        new_tops = []
        for top_node in top_nodes:
            if not add_on_top(new_node, top_node):
                new_tops.append(top_node)
        new_tops.append(new_node)
        top_nodes = new_tops
        
    return top_nodes

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
    return len(cut_nodes)

def print_graph(graph, seen = set()):
    for node in graph:
        if node in seen:
            continue
        print(node.block, [n.block for n in node.prev], [n.block for n in node.next])
        seen.add(node)
        print_graph(node.prev, seen)

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
    #print_graph(graph)
    print("cut nodes", len(lines) - get_cut_nodes(graph))

if __name__ == '__main__':
    main()
