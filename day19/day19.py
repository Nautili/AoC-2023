import sys
import re
import copy
from functools import reduce
from operator import lt, gt, mul

def parse_workflows(workflows):
    parsed_workflows = {}
    for workflow in workflows:
        m = re.search('(.*)\{(.*)}', workflow)
        step_label, steps = m.group(1), m.group(2)
        steps = steps.split(',')
        parsed_steps = []
        for step in steps:
            if '<' in step:
                comp, dest = step.split(':')
                label, val = comp.split('<')
                parsed_steps.append((label, lt, int(val), dest))
            elif '>' in step:
                comp, dest = step.split(':')
                label, val = comp.split('>')
                parsed_steps.append((label, gt, int(val), dest))
            else:
                parsed_steps.append((step,))
        parsed_workflows[step_label] = parsed_steps
    return parsed_workflows

def parse_parts(parts):
    parsed_parts = []
    for part_list in parts:
        part_map = {}
        for part in part_list[1:-1].split(','):
            label, val = part.split('=')
            part_map[label] = int(val)
        parsed_parts.append(part_map)
    return parsed_parts

def run_workflow(workflows, parts_list):
    cur_label = 'in'

    while True:
        if cur_label == 'A':
            return sum(parts_list.values())
        elif cur_label == 'R':
            return 0

        cur_workflow = workflows[cur_label]
        i = 0
        jumped = False
        while not jumped and i < len(cur_workflow):
            step = cur_workflow[i]
            if len(step) == 1:
                cur_label = step[0]
                jumped = True
            else:
                label, op, val, dest = step
                if op(parts_list[label], val):
                    cur_label = dest
                    jumped = True
            i += 1

def get_combos(ranges):
    return reduce(mul, [r - l for l, r in ranges.values()])

def get_good_ranges(cur_label, workflows, ranges):
    if cur_label == 'A':
        return get_combos(ranges)
    if cur_label == 'R':
        return 0

    combos = 0
    for step in workflows[cur_label]:
        if len(step) == 1:
            if step[0] == 'A':
                combos += get_combos(ranges)
            elif step[0] != 'R':
                combos += get_good_ranges(step[0], workflows, ranges)
        else:
            label, op, val, dest = step
            new_ranges = copy.deepcopy(ranges)
            if op == lt:
                new_ranges[label][1] = min(new_ranges[label][1], val)
                ranges[label][0] = max(ranges[label][0], val)
            elif op == gt:
                new_ranges[label][0] = max(new_ranges[label][0], val + 1)
                ranges[label][1] = min(ranges[label][1], val + 1)
            combos += get_good_ranges(dest, workflows, new_ranges)
    return combos

def main():
    with open(sys.argv[1]) as f:
        input = f.read().strip()
    workflows, parts_lists = input.split('\n\n')

    workflows = parse_workflows(workflows.split('\n'))
    parts_lists = parse_parts(parts_lists.split('\n'))
    print(sum(run_workflow(workflows, parts) for parts in parts_lists))

    ranges = {c: [1, 4001] for c in 'xmas'}
    print(get_good_ranges('in', workflows, ranges))

if __name__ == '__main__':
    main()
