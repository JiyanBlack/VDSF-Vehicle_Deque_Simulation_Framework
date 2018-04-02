from Platoon import Platoon
from CAV import CAV
from Model import CAVModel

cavmodel = CAVModel()


class Simulation():
    def __init__(self, time, simStep):
        self.time = time  # simulation time in seconds
        self.simStep = simStep  # time bewteen each simulation step, in ms, or 1/1000 second
        self.loop_num = time * 1000 // simStep + 1

    def run_cav_simluation(self, n):
        print(
            "Start running CAV simulation: {}-vehicle-platoon with {}ms gap in {} seconds.".
            format(n, self.simStep, self.time))
        p = Platoon(self.loop_num)
        for i in range(n):
            p.add_vehicle(
                CAV(idx=i, CAVModel=cavmodel, simulationStep=self.simStep))
        p.deque()
        print("CAV simulation finished.")

    def cav_sim_visualization(self, p):
        pass


sim = Simulation(200, 10)
sim.run_cav_simluation(50)