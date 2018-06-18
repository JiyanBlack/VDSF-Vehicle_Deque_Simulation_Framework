from Objects.Vehicle import Vehicle

class CAV(Vehicle):
    def __init__(self, idx, model, simulationStep, leader=None, paras={}):
        super().__init__(idx, leader, simulationStep, max_v=paras['v_intend'])
        self.tsys = paras['tsys']  # system response time setting for autonomous vehicles in eq6
        self.model = model
        self.vi = self.max_v  # intended speed in m/s, not km/h
        self.max_acc = paras['max_acc']  # maximum acceleration capacity
        self.max_dec = paras['max_dec']  # maximum deceleration capacity
        self.start_timestamp = None # start accelerating timestamp

    def update(self):
        self.base_update()
        time = self.simulationStep / 1000
        new_a = self.max_dec
        if not self.maxBraking:
            new_a = self.model.get_acc(self)
        new_v = self.v + time/2 * (new_a + self.a) 
        new_loc = self.loc + time/2 * (new_v + self.v) 
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
