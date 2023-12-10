import sys

def get_next(l):
    if all(num == 0 for num in l):
        return 0
    return l[-1] + get_next([n2 - n1 for n1, n2 in zip(l, l[1:])])

def main():
    with open(sys.argv[1]) as f:
        lines = [[int(val) for val in line.split()] for line in f.readlines()]
    print(sum(get_next(line) for line in lines))
    print(sum(get_next(list(reversed(line))) for line in lines))

if __name__ == '__main__':
    main()
