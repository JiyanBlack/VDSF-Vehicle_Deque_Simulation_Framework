from Objects.Vehicle import Vehicle
from numpy import random as random


class Gipps_Vehicle(Vehicle):
    def __init__(self,
                 idx,
                 v_intend,
                 gipps,
                 leader=None,
                 driver_reaction_time=2 / 3,
                 randomness=False):
        super().__init__(
            idx,
            leader,
            simulationStep=driver_reaction_time * 1000,
            max_v=v_intend)
        an = 1.7
        sn = 7 # effective size of the vehicle: 5(length) + 2(mini inter-vechile distance)
        bn = -2*an
        if randomness:
            self.an = self.pick_normal(an, 0.3)
            self.sn = self.pick_normal(sn, 0.3)
        else:
            self.an = an
            self.sn = sn
        self.vi = self.max_v  # indended speed, in m/s
        self.bn = bn  # max deceleration
        self.tn = driver_reaction_time  # the reaction time of driver, default is 2/3
        self.b_hat = min(-3.0, (self.bn - 3) / 2)
        self.model = gipps

    def pick_normal(self, mean, std):
        return random.normal(mean, std, 1)[0]

    def update(self):
        self.base_update()
        if self.maxBraking:
            new_a = self.bn
            new_v = self.v + new_a * self.tn
        else:
            new_v = self.model.get_speed(self)
        if new_v < 0:
            new_v = 0
        new_a = (new_v - self.v) / self.tn
        new_loc = self.loc + new_v * self.tn
        self.a = new_a
        self.v = new_v
        self.loc = new_loc