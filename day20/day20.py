import sys
from abc import ABC, abstractmethod
from collections import deque

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

    def toggle(self, signal, sender):
        self.inputs[sender] = signal
        return int(any(input == 0 for input in self.inputs.values()))

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

def signal_n_times(module_map, n):
    counts = [0, 0]
    for i in range(n):
        #if i % 1000000 == 0:
        #    print(i)
        signal_queue = deque()
        signal_queue.append((module_map['broadcaster'], 0, None))
        while signal_queue:
            module, in_signal, sender = signal_queue.popleft()
            #print(sender, in_signal, module.label)
            counts[in_signal] += 1
            if module.label == 'rx' and in_signal == 0:
                return i

            out_signal = module.toggle(in_signal, sender)
            if out_signal != None:
                for output in module.outputs:
                    signal_queue.append((module_map[output], out_signal, module.label))
    return counts[0] * counts[1]

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]

    module_map = build_module(lines)
    #print(signal_n_times(module_map, 1000))
    print("rx", signal_n_times(module_map, 1000000000000000))

if __name__ == '__main__':
    main()
