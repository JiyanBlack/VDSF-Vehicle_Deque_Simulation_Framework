from Objects.Vehicle import Vehicle


class JYVeh(Vehicle):
    def __init__(self, idx, model, simulationStep, v_intend, leader=None):
        super().__init__(idx, leader, simulationStep, max_v=v_intend)
        self.tsys = 0.5  # system response time setting for autonomous vehicles in eq6
        self.model = model
        self.vi = self.max_v  # intended speed in m/s, not km/h
        self.comf_acc = 1  # comfort acceleration
        self.comf_dec = -1  # comfort deceleration
        self.max_acc = 2  # maximum acceleration capacity
        self.max_dec = -3  # maximum deceleration capacity
        self.braking_signal = False  # if receive braking signal, re
        self.response_time_braking = 0