class Vehicle:
    def __init__(self, idx, leader, simulationStep, max_v, length=5, miniGap = 2):
        self.idx = idx  # ith vehicle in the queue, start with 0
        self.set_leader(leader)  # the vehicle in front of the vehicle
        self.max_v = max_v
        self.length = length  # the length of the vehicle
        self.miniGap = miniGap  # the minimum gap between vehicles
        self.simulationStep = simulationStep  # simulation step in ms (1/1000 of a second)
        self.simTime = 0  # time since simulation starts, in ms
        self.maxBraking = False  # should the vechile start sunddenly braking
        # the position of vehicle, the position of the 1st vehicle's rear bumper is 0.
        # For vehicles in the queue, it is negative. For vehile across the stop line, it is positive.
        self.loc = self.calc_loc()
        self.init_loc = self.calc_loc()
        self.a = 0  # acceleration, in m/s
        self.v = 0  # velocity, in m/s
        self.h = 0  # headway, in s
        self.records = {}
        self.delay = 0
        self.follower = None
        self.prev_loc = 0
        self.time_pass_zero = None  # time passes loc = 0 point, in ms
        self.headway_pass_zero = None
        self.speed_pass_zero = None

    def set_leader(self, leader):
        self.leader = leader
        if leader:
            leader.follower = self

    def calc_loc(self):
        if self.leader:
            return self.leader.loc - self.miniGap - self.leader.length
        return 0

    def start_sundden_braking(self):
        self.maxBraking = True

    def stop_sundden_braking(self):
        self.maxBraking = False

    def writeInfo(self):
        '''
        write current vehicle info to a python dictionary, 
        columns are a, v, loc
        indexes are simTime of each simluation step
        '''
        locdiff = (self.loc - self.init_loc)
        if locdiff > 0:
            self.delay = (self.simTime / 1000 - locdiff / self.max_v) / locdiff
        self.h = 0
        if self.leader and self.v > 0:
            self.h = (self.leader.loc - self.loc) / self.v
        records = [self.a, self.v, self.loc, self.h, self.delay]
        self.records[self.simTime] = list(
            map(lambda x: round(x, 4), records))
        self.simTime += self.simulationStep

    def base_update(self):
        self.writeInfo()
        # judge if hit the previous vehicle
        if self.leader:
            spacing = self.leader.loc - self.loc - self.leader.length
            if spacing <= 0:
                print("Vehicle", self.idx, "hit the leader vehicle!")
        if self.time_pass_zero == None and self.loc >= 0:
            self.time_pass_zero = self.simTime
            self.headway_pass_zero = self.h
            self.speed_pass_zero = self.v
    
