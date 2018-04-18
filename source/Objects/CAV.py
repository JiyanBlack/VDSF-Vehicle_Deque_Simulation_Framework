from Objects.Vehicle import Vehicle


class CAV(Vehicle):
    def __init__(self, idx, simulationStep, v_intend, model=None, leader=None):
        super().__init__(idx, leader, simulationStep, max_v=v_intend)
        self.tsys = 0.5  # system response time setting for autonomous vehicles in eq6
        self.model = model
        self.vi = self.max_v  # intended speed in m/s, not km/h
        self.max_acc = 2  # maximum acceleration capacity
        self.max_dec = -3  # maximum deceleration capacity

    def update(self):
        self.base_update()
        time = self.simulationStep / 1000
        new_v = self.model.get_new_v(self)
        new_a = (new_v - self.v) / time
        new_loc = self.loc + new_v * time
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
