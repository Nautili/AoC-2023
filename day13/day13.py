import sys

def get_vertical_mirrors(lines):
    col_counts = {col: 0 for col in range(1, len(lines[0]))}
    for row in lines:
        for i in range(1, len(row)):
            if all(a == b for a, b in zip(row[:i][::-1], row[i:])):
                col_counts[i] += 1
    return col_counts

# offset for smudged mirrors
def get_mirror(lines, offset=0):
    col_counts = get_vertical_mirrors(lines)
    for col, count in col_counts.items():
        if count == len(lines) - offset:
            return col

    # there's probably a builtin for this
    transpose = []
    for col in range(len(lines[0])):
        transpose.append(''.join(line[col] for line in lines))

    col_counts = get_vertical_mirrors(transpose)
    for col, count in col_counts.items():
        if count == len(lines[0]) - offset:
            return 100 * col

def main():
    with open(sys.argv[1]) as f:
        lines = f.read().split("\n\n")
    
    grids = [line.strip().split("\n") for line in lines]
    print(sum(get_mirror(grid) for grid in grids))
    print(sum(get_mirror(grid, 1) for grid in grids))

if __name__ == '__main__':
    main()
