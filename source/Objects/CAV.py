from Objects.Vehicle import Vehicle


class CAV(Vehicle):
    def __init__(self, idx, model, simulationStep, v_intend, leader=None, maxAcc=[]):
        super().__init__(idx, leader, simulationStep, max_v=v_intend)
        self.tsys = 0.5  # system response time setting for autonomous vehicles in eq6
        self.model = model
        self.t_lag_plus = 0.2
        self.t_lag_minus = 0.4
        self.vi = self.max_v  # intended speed in m/s, not km/h
        if maxAcc:
            self.max_acc = maxAcc[0]  # maximum acceleration capacity
            self.max_dec = maxAcc[1]  # maximum deceleration capacity
        else:
            self.max_acc = 1.34  # maximum acceleration capacity
            self.max_dec = -1.34  # maximum deceleration capacity
        self.start_timestamp = None # start accelerating timestamp

    def update(self):
        self.base_update()
        time = self.simulationStep / 1000
        new_a = self.max_dec
        if not self.maxBraking:
            new_a = self.model.get_acc(self)
        new_v = self.v + new_a * time
        new_loc = self.loc + new_v * time
        self.prev_loc = self.loc
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
