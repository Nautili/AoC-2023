import sys

def get_total_distance(map, expansion_factor):
    offsets = [0] * len(map[0])
    for col in range(len(map[0])):
        if col > 0:
            offsets[col] = offsets[col - 1]
        if all(row[col] == '.' for row in map):
            offsets[col] += expansion_factor - 1
    
    galaxies = []
    row_offset = 0
    for row_idx, row in enumerate(map):
        if all(c == '.' for c in row):
            row_offset += expansion_factor - 1
            continue

        for col_idx, val in enumerate(row):
            if val == '#':
                galaxies.append((row_idx + row_offset, col_idx + offsets[col_idx]))

    total_distance = 0
    for r1, c1 in galaxies:
        for r2, c2 in galaxies:
            total_distance += abs(r1 - r2) + abs(c1 - c2)

    return total_distance // 2

def main():
    with open(sys.argv[1]) as f:
        map = [line.strip() for line in f.readlines()]

    print(get_total_distance(map, 2))
    print(get_total_distance(map, 1000000))

if __name__ == '__main__':
    main()
