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
        self.max_v = max_v
        self.records = {}
        self.delay = -1
        self.follower = None
        self.prev_loc = 0
        self.time_pass_zero = -1  # time passes loc = 0 point, in ms

    def set_leader(self, leader):
        self.leader = leader
        leader.follower = self

    def calc_loc(self):
        return -self.idx * (self.miniGap + self.length)

    def start_sundden_braking(self):
        self.maxBraking = True

    def stop_sundden_braking(self):
        self.maxBraking = False

    def get_time_pass_zero(self):
        return self.time_pass_zero / 1000

    def writeInfo(self):
        '''
        write current vehicle info to a python dictionary, 
        columns are a, v, loc
        indexes are simTime of each simluation step
        '''
        self.delay = self.simTime / 1000 - (
            self.loc - self.calc_loc()) / self.max_v
        records = [self.a, self.v, self.loc]
        headway = 0
        if self.leader and self.v > 0:
            headway = (self.leader.loc - self.loc) / self.v
        records.append(headway)
        self.records[self.simTime] = list(
            map(lambda x: round(x, 3), records))
        self.simTime += self.simulationStep

    def base_update(self):
        self.writeInfo()
        # judge if hit the previous vehicle
        if self.leader:
            spacing = self.leader.loc - self.loc - self.leader.length
            if spacing <= 0:
                print("Vehicle", self.idx, "hit the leader vehicle!")
        if self.time_pass_zero < 0 and self.loc >= 0:
            self.time_pass_zero = self.simTime
