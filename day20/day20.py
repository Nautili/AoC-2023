import sys
from abc import ABC, abstractmethod
from collections import deque
from functools import reduce
from math import gcd

class Module(ABC):
    def __init__(self, label, outputs):
        self.label = label
        self.outputs = outputs
    
    @abstractmethod
    def toggle(self, signal, sender):
        return NotImplemented

class BroadcastModule(Module):
    def toggle(self, signal, sender):
        return signal

class FlipFlopModule(Module):
    def __init__(self, label, outputs):
        super().__init__(label, outputs)
        self.state = 0

    def toggle(self, signal, sender):
        if signal == 1:
            return None
        self.state = 1 - self.state
        return self.state

class ConjunctionModule(Module):
    def __init__(self, label, outputs, inputs):
        super().__init__(label, outputs)
        self.inputs = {input : 0 for input in inputs}
        self.toggled = False

    def toggle(self, signal, sender):
        if signal == 1:
            self.toggled = True
        self.inputs[sender] = signal
        return int(any(input == 0 for input in self.inputs.values()))

    def was_toggled(self):
        was_toggled = self.toggled
        self.toggled = False
        return was_toggled

def get_inputs(lines, label):
    inputs = []
    for line in lines:
        line = line.split(' ')
        outputs = [dest.strip(',') for dest in line[2:]]
        if label in outputs:
            inputs.append(line[0][1:])
    return inputs

def build_module(lines):
    modules = []
    all_outputs = set()
    for line in lines:
        line = line.split(' ')
        outputs = [dest.strip(',') for dest in line[2:]]
        all_outputs.update(outputs)

        if line[0] == 'broadcaster':
            modules.append(BroadcastModule('broadcaster', outputs))
        elif line[0][0] == '%':
            label = line[0][1:]
            modules.append(FlipFlopModule(label, outputs))
        elif line[0][0] == '&':
            label = line[0][1:]
            modules.append(ConjunctionModule(label, outputs, get_inputs(lines, label)))

    module_map = {}
    for module in modules:
        module_map[module.label] = module
    for output in all_outputs:
        if output not in module_map:
            module_map[output] = BroadcastModule(output, [])
    return module_map

def press_button(module_map, counts):
    signal_queue = deque()
    signal_queue.append((module_map['broadcaster'], 0, None))
    while signal_queue:
        module, in_signal, sender = signal_queue.popleft()
        # debug
        #print(sender, in_signal, module.label)
        counts[in_signal] += 1

        out_signal = module.toggle(in_signal, sender)
        if out_signal != None:
            for output in module.outputs:
                signal_queue.append((module_map[output], out_signal, module.label))

def signal_n_times(module_map, n):
    counts = [0, 0]
    for i in range(n):
        press_button(module_map, counts)
    return counts[0] * counts[1]

def lcm(a, b):
    return a * b // gcd(a, b)

def get_earliest_rx(module_map):
    for label, module in module_map.items():
        if 'rx' in module.outputs:
            target_module = module

    cycle_lengths = []
    cycle = 1
    while len(cycle_lengths) < len(target_module.inputs):
        press_button(module_map, [0, 0])
        if target_module.was_toggled():
            cycle_lengths += [cycle]
        cycle += 1

    return reduce(lcm, cycle_lengths)

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    print(signal_n_times(build_module(lines), 1000))
    print(get_earliest_rx(build_module(lines)))

if __name__ == '__main__':
    main()
