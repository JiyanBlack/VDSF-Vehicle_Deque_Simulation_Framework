from Objects.Platoon import Platoon
from Objects.CAV import CAV
from Objects.Models.CAVModel import CAVModel
from Objects.Models.ACDA import ACDAModel
from Objects.Gipps_Vehicle import Gipps_Vehicle
from Objects.Models.GippsModel import GippsModel
from Objects.Models.IDM import IDM
import math


class Simulation():
    def __init__(self, time, avStep = 100):
        self.time = time  # simulation time in seconds
        self.cavmodel = CAVModel()  # CAV model
        self.gipps = GippsModel()  # Gipps model
        self.acda = ACDAModel()  # ACDA model
        self.idm = IDM()
        self.avStep = avStep
        self.gippsStep = 2/3 * 1000

    def get_cav_loop_num(self, time):
        return math.ceil(time * 1000 / self.avStep)

    def run_cav_simluation(self, n, intend_speed, ACDA=False, maxAcc = []):
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        if ACDA:
            themodel  = self.idm
        else:
            themodel = self.cavmodel
        for i in range(n):
            p.add_vehicle(
                CAV(idx=i,
                    model=themodel,
                    simulationStep=self.avStep,
                    v_intend=intend_speed,
                    maxAcc = maxAcc))
        p.run(loop_num)
        return p

    def run_cav_simluation_with_braking(self,
                                        n,
                                        intend_speed,
                                        sim_length_after_stop,
                                        stop_veh_idx=0,
                                        ACDA=False,
                                        HSR_mode = False):
        p = self.run_cav_simluation(n, intend_speed, ACDA, HSR_mode)
        # print("Vehicle {} start maximum deceleration...".format(stop_veh_idx))
        p.platoon[stop_veh_idx].start_sundden_braking()
        new_loop_num = self.get_cav_loop_num(sim_length_after_stop)
        p.run(new_loop_num)
        # print("Braking simulation finishes.")
        return p

    def get_gipps_loop_num(self, time, driver_reaction_time):
        return math.ceil(time / driver_reaction_time)

    def run_gipps_simluation(self,
                             n,
                             intend_speed,
                             randomness=False,
                             driver_reaction_time=2 / 3):
        # print(
        #     "Start running human-driver simulation (Gipps Model): {}-vehicle-platoon with {}s reaction time in {} seconds.".
        #     format(n, driver_reaction_time, self.time))
        loop_num = self.get_gipps_loop_num(self.time, driver_reaction_time)
        p = Platoon()
        for i in range(n):
            p.add_vehicle(
                Gipps_Vehicle(
                    idx=i,
                    gipps=self.gipps,
                    driver_reaction_time=driver_reaction_time,
                    v_intend=intend_speed,
                    randomness=randomness))
        p.run(loop_num)
        # print("Human-driver simulation (Gipps Model) deque finished.")
        return p

    def run_gipps_simluation_with_braking(self,
                                          n,
                                          intend_speed,
                                          sim_length_after_stop,
                                          stop_veh_idx=0,
                                          randomness=False,
                                          driver_reaction_time=2 / 3):
        p = self.run_gipps_simluation(n, intend_speed, randomness,
                                      driver_reaction_time)
        # print("Vehicle {} start maximum deceleration...".format(stop_veh_idx))
        p.platoon[stop_veh_idx].start_sundden_braking()
        new_loop_num = self.get_gipps_loop_num(sim_length_after_stop,
                                               driver_reaction_time)
        p.run(new_loop_num)
        # print("Braking simulation finishes.")
        return p
