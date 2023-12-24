import sys

def dot(v1, v2):
    return sum(l * r for l, r in zip(v1, v2))

def det(arr):
    return arr[0][0] * arr[1][1] - arr[0][1] * arr[1][0]

def add(p1, p2):
    return tuple(l + r for l, r in zip(p1, p2))

def sub(p1, p2):
    return tuple(l - r for l, r in zip(p1, p2))

def mul(v, s):
    return tuple(s * val for val in v)

def get_intersection(l1, l2):
    p1, v1 = l1
    p2, v2 = l2
    denominator = det([[dot(v1, v1), -dot(v1, v2)],
                       [dot(v1, v2), -dot(v2, v2)]])
    if denominator == 0:
        # this is parallel, so treat it as though it's in the past
        return False, (0, 0)

    s_numerator = det([[dot(v1, sub(p2, p1)), -dot(v1, v2)],
                       [dot(v2, sub(p2, p1)), -dot(v2, v2)]])
    t_numerator = det([[dot(v1, v1), dot(v1, sub(p2, p1))],
                       [dot(v1, v2), dot(v2, sub(p2, p1))]])
    s = s_numerator / denominator
    t = t_numerator / denominator
    is_valid = s >= 0 and t >= 0
    return is_valid, add(p1, mul(v1, s_numerator / denominator))

def get_z_projection(lines):
    return [[(point[0], point[1], 0), (vec[0], vec[1], 0)] for point, vec in lines]

def get_in_bounds(lines, lo, hi):
    in_bounds = 0
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            is_valid, point = get_intersection(lines[i], lines[j])
            if is_valid and lo <= point[0] <= hi and lo <= point[1] <= hi:
                in_bounds += 1
    return in_bounds

def get_lines(lines):
    out_lines = []
    for line in lines:
        front, back = line.split('@')
        out_lines.append([tuple(int(val.strip()) for val in front.split(',')),
                          tuple(int(val.strip()) for val in back.split(','))])
    return out_lines

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    line_defs = get_lines(lines)
    orth_proj = get_z_projection(line_defs)
    low_bound = 200000000000000
    high_bound = 400000000000000
    print(get_in_bounds(orth_proj, low_bound, high_bound))

if __name__ == '__main__':
    main()
