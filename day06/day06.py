import sys
import math
from functools import reduce
from operator import mul

def get_winning_count(time, distance):
    m = time / 2
    d = math.sqrt(m * m - distance)

    return math.ceil(m + d) - math.floor(m - d) - 1

def main():
    with open(sys.argv[1]) as f:
        times = list(map(int, f.readline().split()[1:]))
        distances = list(map(int, f.readline().split()[1:]))

    valid_answers = [get_winning_count(time, distance) for time, distance in zip(times, distances)]
    print(reduce(mul, valid_answers)) 

    new_time = int(''.join(map(str, times)))
    new_distance = int(''.join(map(str, distances)))
    print(get_winning_count(new_time, new_distance))

if __name__ == '__main__':
    main()
