import sys

def get_vertices(dirs):
    dir_map = {
        "R": (0, 1),
        "D": (1, 0),
        "L": (0, -1),
        "U": (-1, 0),
    }

    vertices = [(1, 1)]
    for dir, dist in dirs:
        vertices.append((vertices[-1][0] + dir_map[dir][0] * dist, 
                         vertices[-1][1] + dir_map[dir][1] * dist))
    return vertices

#code format is '(#dddddd)'
def get_dir(code):
    return ("RDLU"[int(code[-2])], int(code[2:-2], 16))

def get_lagoon_size(dirs):
    border = sum(dir[1] for dir in dirs) + 2
    verts = get_vertices(dirs)
    return (border + abs(sum(l[0] * r[1] - l[1] * r[0] for l, r in zip(verts, verts[1:])))) // 2

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    dirs = []
    hex_dirs = []
    for line in lines:
        dir, dist, color = line.split()
        dirs.append((dir, int(dist)))
        hex_dirs.append(get_dir(color))
    print(get_lagoon_size(dirs))
    print(get_lagoon_size(hex_dirs))

if __name__ == '__main__':
    main()
