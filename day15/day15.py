import sys

def hash(s):
    cur_val = 0
    for c in s:
        cur_val = ((cur_val + ord(c)) * 17) % 256
    return cur_val

class Hashmap:
    def __init__(self):
        self.boxes = [{} for _ in range(256)]

    def run(self, op):
        if '=' in op:
            label, val = op.split('=')
            self.boxes[hash(label)][label] = int(val)
        else:
            label = op[:-1]
            if label in self.boxes[hash(label)]:
                del(self.boxes[hash(label)][label])

    def get_focus(self):
        focus = 0
        for n in range(len(self.boxes)):
            for slot, val in enumerate(self.boxes[n].values()):
                focus += (n + 1) * (slot + 1) * val
        return focus

def main():
    with open(sys.argv[1]) as f:
        input = f.readline().strip().split(',')

    print(sum(hash(s) for s in input))

    hashmap = Hashmap()
    for s in input:
        hashmap.run(s)
    print(hashmap.get_focus())

if __name__ == '__main__':
    main()
