class Vehicle:
    def __init__(self, idx, leader, simulationStep, max_v):
        self.idx = idx  # ith vehicle in the queue, start with 0
        self.leader = leader  # the vehicle in front of the vehicle
        self.a = 0  # acceleration, in m/s
        self.v = 0  # velocity, in m/s
        self.length = 5  # the length of the vehicle
        self.miniGap = 2  # the minimum gap between vehicles
        self.simulationStep = simulationStep  # simulation step in ms (1/1000 of a second)
        self.simTime = 0  # time since simulation starts, in ms
        self.maxBraking = False  # should the vechile start sunddenly braking
        # the position of vehicle, the position of the 1st vehicle's rear bumper is 0.
        # For vehicles in the queue, it is negative. For vehile across the stop line, it is positive.
        self.loc = self.calc_loc()
        self.set_state = False
        self.set_loop_num = 0
        self.max_v = max_v
        self.records = {}
        self.delay = -1

    def set_leader(self, leader):
        self.leader = leader

    def calc_loc(self):
        return -self.idx * (self.miniGap + self.length)

    def set_braking_state_after_loops(self, state, loop_num):
        self.set_state = state
        self.set_loop_num = loop_num

    def start_sundden_braking(self):
        self.set_braking_state_after_loops(True, 0)

    def stop_sundden_braking(self):
        self.set_braking_state_after_loops(False, 0)

    def writeInfo(self):
        '''
        write current vehicle info to a python dictionary, 
        columns are a, v, loc
        indexes are simTime of each simluation step
        '''
        self.delay = self.simTime / 1000 - (
            self.loc - self.calc_loc()) / self.max_v
        self.records[self.simTime] = list(
            map(lambda x: round(x, 3), [self.a, self.v, self.loc]))
        self.simTime += self.simulationStep

    def base_update(self):
        self.writeInfo()
        if self.set_loop_num <= 0 and (self.maxBraking != self.set_state):
            self.maxBraking = self.set_state
        if self.set_loop_num > 0:
            self.set_loop_num -= 1
