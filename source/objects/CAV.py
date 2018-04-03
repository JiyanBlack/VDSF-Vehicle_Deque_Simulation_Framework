from Objects.Vehicle import Vehicle


class CAV(Vehicle):
    def __init__(self, idx, CAVModel, simulationStep, leader=None):
        super().__init__(idx, leader, simulationStep)
        self.tsys = 0.5  # system response time setting for autonomous vehicles in eq6
        self.CAVModel = CAVModel

    def calc_acc(self):
        return self.CAVModel.get_acc(self)

    def update(self):
        self.writeInfo()
        new_a = self.calc_acc()
        new_v = self.v + new_a * self.simulationStep / 1000
        new_loc = self.loc + new_v * self.simulationStep / 1000
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
