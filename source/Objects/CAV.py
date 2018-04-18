from Objects.Vehicle import Vehicle


class CAV(Vehicle):
    def __init__(self, idx, model, simulationStep, v_intend, leader=None):
        super().__init__(idx, leader, simulationStep, max_v=v_intend)
        self.tsys = 0.5  # system response time setting for autonomous vehicles in eq6
        self.model = model
        self.vi = self.max_v  # intended speed in m/s, not km/h
        self.comf_acc = 0.58  # comfort acceleration
        self.max_acc = 2  # maximum acceleration capacity
        self.max_dec = -3  # maximum deceleration capacity
        self.braking_signal = False  # if receive braking signal, vehicle starts to decelerate at speed and comfort dec.
        self.max_braking_response_time = 0.1  # test the braking response time (maximum)
        self.braking_timestamp = -1
        self.h = 0.2  # the system for platoon operation
        self.connected = True
        self.follower_recom_dec = -1

    def calc_smooth_braking(self):
        pass

    def braking_signal_on(self):
        self.braking_signal = True
        car = self
        bt = self.simTime
        while car.leader:
            bt += car.max_braking_response_time * 1000
        self.braking_timestamp = bt

    def get_comf_dec(self):
        if not self.leader:
            self.comf_dec = -0.54  # comfort deceleration
            return
        vl0 = self.leader.v
        v0 = self.v
        alm = self.leader.comf_dec
        ap = self.a
        tr = self.max_braking_response_time

        def calc_am(tb):
            am = (vl0 + alm * tr + alm * tb - v0 - ap * tr) / tb
            return am
                    

    def update(self):
        self.base_update()
        time = self.simulationStep / 1000
        new_a = self.model.get_acc(self)
        if self.braking_timestamp > 0 and self.simTime > self.braking_timestamp:
            new_a = self.get_dec_idx()
        new_v = self.v + new_a * time
        new_loc = self.loc + new_v * time
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
