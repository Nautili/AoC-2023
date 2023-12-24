import sys
import z3

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

def get_projection(lines, mask):
    new_lines = []
    for point, vec in lines:
        new_point = tuple(l * r for l, r in zip(point, mask))
        new_vec = tuple(l * r for l, r in zip(vec, mask))
        new_lines.append((new_point, new_vec))
    return new_lines

def get_intersections(lines):
    intersections = set()
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            is_valid, point = get_intersection(lines[i], lines[j])
            if is_valid:
                intersections.add(point)
    return intersections

def get_in_bounds(lines, lo, hi):
    points = get_intersections(lines)
    return sum(lo <= point[0] <= hi and lo <= point[1] <= hi for point in points)

def solve_intersecting_throw(lines):
    p = z3.RealVector("p", 3)
    v = z3.RealVector("v", 3)
    t = z3.RealVector("t", 3)

    s = z3.Solver()
    for t_i, line in enumerate(lines[:3]):
        point, vec = line
        for i in range(3):
            s.add(p[i] + v[i] * t[t_i] == point[i] + vec[i] * t[t_i])

    if s.check() == z3.sat:
        return sum(s.model()[val].as_long() for val in p)

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
    orth_proj = get_projection(line_defs, (1, 1, 0))
    low_bound = 200000000000000
    high_bound = 400000000000000
    print(get_in_bounds(orth_proj, low_bound, high_bound))
    print(solve_intersecting_throw(line_defs))

if __name__ == '__main__':
    main()
