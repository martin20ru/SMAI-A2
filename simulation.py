#
# Informed Search Methods
#
# Machine simulator.
# You do not want to change anything in here!
#

from timeit import default_timer as timer

class Simulation:

    def __init__(self, num_gates, num_cars, capacity):
        assert( num_gates > 0 )
        assert( num_cars > 0 )
        assert( capacity > 0 )
        self.capacity = capacity
        self.assign_func = None
        self.max_time = 0
        self.tick = 0
        self.gates = [0 for _ in range(num_gates)]
        self.cars  = [0 for _ in range(num_cars)]
        self.boxes = []
        self.total_time = 0

    def __str__(self):
        s = 'T: ' + str(self.tick)
        s += '\nC: '
        for c in self.cars:
            s +=  ' ' + str(c)
        s += '\nG: '
        for g in self.gates:
            s +=  ' ' + str(g)
        s += '\nB: ' + str(self.boxes) + '\n'
        return s

    def reset(self, assign_func, max_time):
        self.tick = 0
        for c in range(len(self.cars)):
            self.cars[c] = 0
        for g in range(len(self.gates)):
            self.gates[g] = 0
        self.boxes = []
        self.total_time = 0
        self.assign_func = assign_func
        self.max_time = max_time
        return

    def step(self, weight):
        assert(self.assign_func != None)
        assert(weight >= 0)
        filled = False
        if self.cars[0] > 0:
            start = timer()
            gate = self.assign_func( self.cars.copy(), self.gates.copy(), self.capacity, self.max_time)
            end = timer()
            self.total_time += (end-start)
            assert(0 <= gate < len(self.gates))
            if self.max_time > 0 and ( end - start) > (1.05 * self.max_time):
                print('Warning: assignment took to long, assigning to box at gate 0.', end-start)
                gate = 0
            self.gates[gate] += self.cars[0]
            if self.gates[gate] > self.capacity:
                self.boxes.append(self.gates[gate])
                self.gates[gate] = 0
                filled = True
        self.cars.pop(0)
        self.cars.append(weight)
        self.tick += 1
        return filled

    def get_boxes(self ):
        return self.boxes

    def get_tick(self):
        return self.tick

    def get_capacity(self):
        return self.capacity

    def get_cars(self):
        return self.cars

    def get_gates(self):
        return self.gates

    def get_total_time(self):
        return self.total_time
