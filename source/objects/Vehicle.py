class Vehicle:
    def __init__(self, idx, leader, simulationStep):
        self.idx = idx  # ith vehicle in the queue, start with 0
        self.leader = leader  # the vehicle in front of the vehicle
        self.a = 0  # acceleration, in m/s
        self.v = 0  # velocity, in m/s
        self.max_acc = 3  # maximum acceleration capacity
        self.max_dec = -3  # maximum deceleration capacity
        self.comfort_acc = 1  # comfort acceleration
        self.comfort_dec = -1  # comfort deceleration
        self.length = 2  # the length of the vehicle
        self.miniGap = 2  # the minimum gap between vehicles
        self.v_intend = 22  # intended speed 22 m/s = 80 km/h
        self.simulationStep = simulationStep  # simulation step in ms (1/1000 of a second)
        self.simTime = 0  # time since simulation starts
        self.records = {}
        # the position of vehicle, the position of the 1st vehicle's front bumper is 0.
        # For vehicles in the queue, it is negative. For vehile across the stop line, it is positive.
        self.loc = self.calc_loc()

    def calc_acc(self):
        pass

    def set_leader(self, leader):
        self.leader = leader

    def calc_loc(self):
        return -self.idx * (self.miniGap + self.length)

    def writeInfo(self):
        '''
        write current vehicle info to a python dictionary, 
        columns are a, v, loc
        indexes are simTime of each simluation step
        '''
        self.records[self.simTime] = list(
            map(lambda x: round(x, 3), [self.a, self.v, self.loc]))
        self.simTime += self.simulationStep

    def update(self):
        pass
