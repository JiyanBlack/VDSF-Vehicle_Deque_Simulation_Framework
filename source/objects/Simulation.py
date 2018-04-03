from Objects.Platoon import Platoon
from Objects.CAV import CAV
from Objects.Model import CAVModel


class Simulation():
    def __init__(self, time, simStep):
        self.time = time  # simulation time in seconds
        self.simStep = simStep  # time bewteen each simulation step, in ms, or 1/1000 second
        self.loop_num = time * 1000 // simStep + 1
        self.cavmodel = CAVModel()

    def run_cav_simluation(self, n):
        print(
            "Start running CAV simulation: {}-vehicle-platoon with {}ms gap in {} seconds.".
            format(n, self.simStep, self.time))
        p = Platoon(self.loop_num)
        for i in range(n):
            p.add_vehicle(
                CAV(idx=i, CAVModel=self.cavmodel,
                    simulationStep=self.simStep))
        p.deque()
        print("CAV simulation finished.")
        return p
