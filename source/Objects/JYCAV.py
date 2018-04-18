from Objects.CAV import CAV


class JYCAV(CAV):
    def __init__(self,
                 idx,
                 simulationStep,
                 v_intend,
                 cavmodel,
                 jymodel,
                 leader=None):
        super().__init__(idx, simulationStep, v_intend)
        self.max_braking_response_time = 0.1  # test the braking response time (maximum)
        self.real_braking_response_time = 0
        self.braking_timestamp = -1
        self.h = 0.2  # the headway for platoon operation
        self.comf_dec = -0.54
        self.comf_acc = 0.58
        self.cavmodel = cavmodel
        self.jymodel = jymodel
        self.model = jymodel
        self.comf_braking = False
        self.a_at_signal = -1

    def braking_signal_on(self):
        # real braking time stamp, in ms
        self.braking_timestamp = self.simTime + self.real_braking_response_time * 1000
        self.a_at_signal = self.a
        self.comf_dec = self.cal_dec()

    def cal_dec(self):
        car = self
        if not car.leader:
            return car.comf_dec  # comfort deceleration
        vl0 = car.leader.v
        v0 = car.v
        alm = car.leader.comf_dec
        ap = car.a
        tr = car.max_braking_response_time

        vl1 = vl0 + alm * tr
        v1 = v0 + ap * tr

        dx0 = car.leader.loc - car.loc - car.leader.length
        dx1 = dx0 + vl0 * tr + 0.5 * alm * tr * tr - (
            v0 * tr + 0.5 * ap * tr * tr)
        tb = (4 - 2 * dx1) / (vl1 - v1)
        am = (vl1 - v1 + alm * tb) / tb
        return am

    def choose_model(self):
        comf_dec = self.cal_dec()
        if comf_dec <= self.max_dec:
            print("Platoon breaks at {} vehicle for dec {}.".format(
                self.idx, comf_dec))
            self.model = self.cavmodel

    def update(self):
        self.base_update()
        # self.choose_model()
        time = self.simulationStep / 1000
        new_v = self.model.get_new_v(self)
        new_a = (new_v - self.v) / time
        new_loc = self.loc + new_v * time
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
