import sys
import random
from copy import deepcopy
from functools import reduce
from operator import mul

def get_vertices(edges):
    vertices = set()
    for s, d in edges:
        vertices.add(s)
        vertices.add(d)
    return vertices

def karger(edges):
    counts = {v: 1 for v in get_vertices(edges)}
    while len(counts) > 2:
        random_edge = deepcopy(random.choice(edges))
        dest_counts = counts[random_edge[1]]
        if random_edge[0] != random_edge[1]:
            counts[random_edge[0]] += dest_counts
            del counts[random_edge[1]]
        edges.remove(random_edge)
        for edge in edges:
            if edge[1] == random_edge[1]:
                edge[1] = random_edge[0]
            if edge[0] == random_edge[1]:
                edge[0] = random_edge[0]
            if edge[1] < edge[0]:
                edge[0], edge[1] = edge[1], edge[0]
    edges = [edge for edge in edges if edge[0] != edge[1]]
    return edges, counts

def find_cut_edges(graph, n):
    edges = []
    for key, adj in graph.items():
        for val in adj:
            edges.append([key, val])

    cut_edges = []
    counts = 0
    while len(cut_edges) != n: 
        cut_edges, counts = karger(deepcopy(edges))
        print(cut_edges, counts)

    return reduce(mul, counts.values())

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    graph = {line.split()[0].strip(':'): line.split()[1:] for line in lines}
    print(find_cut_edges(graph, 3))

if __name__ == '__main__':
    main()
