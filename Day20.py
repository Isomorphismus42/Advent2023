"""
--- Day 20: Pulse Propagation ---

With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the
command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the machines directly,
but rather to communication modules attached to the machines that perform various initialization tasks and also act
as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse,
it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high
pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on
and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input
modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction
module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low
pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of
its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module.
When you push the button, a single low pulse is sent directly to the broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it
again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c,
and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be
handled first.

The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol
identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a

In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules
is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another
module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input,
acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a

After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output

This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module
(inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The
multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to
the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output

Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers
a high pulse from each of its two inputs, pushing the button a second time does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output

Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output

This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is
handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that,
flip-flop b turns off, which causes con to update its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output

This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their
original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (
including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are
sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these
together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent.
Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would be sent after
pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you
get if you multiply the total number of low pulses sent by the total number of high pulses sent?


------------------- Part Two --------------------

The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine
turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press,
what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

"""

import numpy as np
# import heapq
# import re
# from collections import OrderedDict
# import functools
# from shapely.geometry import Polygon
# import math


LOW = False
HIGH = True

modules = dict()
conjunction_modules = set()
pulse_queue = list()


# prefix %
class FlipFlop:
    def __init__(self, name, output_modules):
        self.state = LOW
        self.name = name
        self.output_modules = output_modules

    def receive_pulse(self, pulse, module_name=-1):
        if pulse == LOW:
            self.state = not self.state
            for module in self.output_modules:
                pulse_queue.append((self.state, module, self.name))


# prefix &
class Conjunction:
    def __init__(self, name, output_modules):
        self.name = name
        self.input_modules = dict()
        self.output_modules = output_modules

    def add_input_module(self, module):
        self.input_modules[module] = LOW

    def receive_pulse(self, pulse, module_name):
        self.input_modules[module_name] = pulse
        if len(self.input_modules) == sum(self.input_modules.values()):
            pulse = LOW
        else:
            pulse = HIGH
        for module in self.output_modules:
            pulse_queue.append((pulse, module, self.name))


class Broadcaster:
    def __init__(self, name, output_modules):
        self.name = name
        self.output_modules = output_modules

    def receive_pulse(self, pulse, module_name=-1):
        for module in self.output_modules:
            pulse_queue.append((pulse, module, self.name))


def initialise_modules():
    with open('inputs/input_day20', 'r') as file:
        for line in file:
            name, destinations = line[:-1].split(' -> ')
            destinations = destinations.split(', ')
            if name[0] == '%':
                modules[name[1:]] = FlipFlop(name[1:], destinations)
            elif name[0] == '&':
                modules[name[1:]] = Conjunction(name[1:], destinations)
                conjunction_modules.add(name[1:])
            else:  # Broadcaster
                modules[name] = Broadcaster(name, destinations)
        for module in modules.values():
            for destination in module.output_modules:
                if destination in conjunction_modules:
                    modules[destination].add_input_module(module.name)


def part1():
    initialise_modules()

    count_low_pulses = 0
    count_high_pulses = 0
    for n in range(1000):
        modules['broadcaster'].receive_pulse(LOW)
        count_low_pulses += 1
        # print("button -low-> broadcaster")
        while pulse_queue:
            pulse, module_in, module_out = pulse_queue.pop(0)
            # print(module_out + ' -' + str(pulse) + '-> ' + module_in)
            if pulse:
                count_high_pulses += 1
            else:
                count_low_pulses += 1
            if module_in in modules.keys():
                modules[module_in].receive_pulse(pulse, module_out)
    return count_low_pulses * count_high_pulses


def part2():
    initialise_modules()
    push_count = 0
    ks_circle, jf_circle, qs_circle, zk_circle = 0, 0, 0, 0
    while not (ks_circle and jf_circle and qs_circle and zk_circle):
        modules['broadcaster'].receive_pulse(LOW)
        push_count += 1
        while pulse_queue:
            pulse, module_in, module_out = pulse_queue.pop(0)
            if module_out == 'ks':
                if pulse == HIGH:
                    ks_circle = push_count
            if module_out == 'jf':
                if pulse == HIGH:
                    jf_circle = push_count
            if module_out == 'qs':
                if pulse == HIGH:
                    qs_circle = push_count
            if module_out == 'zk':
                if pulse == HIGH:
                    zk_circle = push_count
            elif module_in != 'rx':
                modules[module_in].receive_pulse(pulse, module_out)
    return np.lcm.reduce([ks_circle, jf_circle, qs_circle, zk_circle], dtype='int64')


if __name__ == "__main__":
    print(part2())
