import sys
import re
from math import gcd

def get_path_length(path, network, cur_node):
    if cur_node not in network:
        print("No valid starting point")
        return

    path_length = 0
    while cur_node[-1] != 'Z':
        if path[path_length % (len(path) - 1)] == 'L':
            cur_node = network[cur_node][0]
        else:
            cur_node = network[cur_node][1]
        path_length += 1
    return path_length

def lcm(a, b):
    return a * b // gcd(a, b)

# It's dumb and "lucky" that this is this simple
def get_path_length_for_ghosts(path, network):
    total_lcm = 1
    for node in network:
        if node[-1] == 'A':
            total_lcm = lcm(total_lcm, get_path_length(path, network, node))
    return total_lcm

def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    path = lines[0]
    network = {node: (left, right) for node, left, right in \
               [re.sub(r'[^\w ]+', '', line).split() for line in lines[2:]]}
    print(get_path_length(path, network, 'AAA'))
    print(get_path_length_for_ghosts(path, network))

if __name__ == '__main__':
    main()
