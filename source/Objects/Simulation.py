from Objects.Platoon import Platoon
from Objects.CAV import CAV
from Objects.Models.CAVModel import CAVModel
from Objects.Models.GippsModel import GippsModel
from Objects.Models.IDM import IDM
from Objects.IDMCar import IDMAV
from Objects.IDMCar import IDMHumanVehicle
from Objects.Gipps_Vehicle import Gipps_Vehicle
import math
import random

class Simulation():
    def __init__(self, time, avStep=100):
        self.time = time  # simulation time in seconds
        self.cavmodel = CAVModel()  # CAV model
        self.gipps = GippsModel()  # Gipps model
        self.idm = IDM()  # IDM
        self.avStep = avStep
        self.av = self.idm
        self.human = self.idm
        self.cav = self.cavmodel

    def get_cav_loop_num(self, time):
        return math.ceil(time * 1000 / self.avStep)

    def run_av_simulation(self, n, paras):
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        leader = None
        for i in range(n):
            newcar = IDMAV(idx=i,
                model=self.av,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        return p

    def run_human_simulation(self, n, paras):
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        leader = None
        for i in range(n):
            newcar = IDMHumanVehicle(idx=i,
                model=self.human,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        return p
    
    def run_cav_simulation(self, n, paras):
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        leader = None
        for i in range(n):
            newcar = CAV(idx=i,
                model=self.cavmodel,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        return p

    def run_first_vehicle_simulation(self,n,paras, firstVeh):
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        leader = None
        if firstVeh == 0:
            newcar = IDMHumanVehicle(idx=0,
                model=self.human,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
        elif firstVeh == 1:
            newcar = IDMAV(idx=0,
                model=self.av,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
        else:
            newcar = CAV(idx=0,
                model=self.cav,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
        p.add_vehicle(newcar)
        leader = newcar
        for i in range(1,n):
            rnd = random.random()
            newcar = IDMHumanVehicle(idx=i,
                model=self.human,
                simulationStep=self.avStep,
                leader=leader,
                paras=paras)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        return p

    def run_mixed_simulation(self,n,paras,ratio):
        # ratio: (human, av, cav)
        loop_num = self.get_cav_loop_num(self.time)
        p = Platoon()
        leader = None
        for i in range(n):
            rnd = random.random()
            if rnd < ratio[0]:
                newcar = IDMHumanVehicle(idx=i,
                    model=self.human,
                    simulationStep=self.avStep,
                    leader=leader,
                    paras=paras)
            elif rnd >= ratio[0] and rnd < (ratio[0] + ratio[1]):
                newcar = IDMAV(idx=i,
                    model=self.av,
                    simulationStep=self.avStep,
                    leader=leader,
                    paras=paras)
            else:
                newcar = CAV(idx=i,
                    model=self.cav,
                    simulationStep=self.avStep,
                    leader=leader,
                    paras=paras)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        return p

    def run_cav_simulation_with_braking(self,
                                        n,
                                        intend_speed,
                                        sim_length_after_stop,
                                        stop_veh_idx=0,
                                        ACDA=False,
                                        HSR_mode=False):
        p = self.run_cav_simluation(n, intend_speed, ACDA, HSR_mode)
        # print("Vehicle {} start maximum deceleration...".format(stop_veh_idx))
        p.platoon[stop_veh_idx].start_sundden_braking()
        new_loop_num = self.get_cav_loop_num(sim_length_after_stop)
        p.run(new_loop_num)
        # print("Braking simulation finishes.")
        return p

    def get_gipps_loop_num(self, time, driver_reaction_time):
        return math.ceil(time / driver_reaction_time)

    def run_gipps_simulation(self,
                             n,
                             intend_speed,
                             randomness=False,
                             driver_reaction_time=2 / 3):
        # print(
        #     "Start running human-driver simulation (Gipps Model): {}-vehicle-platoon with {}s reaction time in {} seconds.".
        #     format(n, driver_reaction_time, self.time))
        loop_num = self.get_gipps_loop_num(self.time, driver_reaction_time)
        p = Platoon()
        leader = None
        for i in range(n):
            newcar = Gipps_Vehicle(
                idx=i,
                gipps=self.gipps,
                driver_reaction_time=driver_reaction_time,
                leader=leader,
                v_intend=intend_speed,
                randomness=randomness)
            p.add_vehicle(newcar)
            leader = newcar
        p.run(loop_num)
        # print("Human-driver simulation (Gipps Model) deque finished.")
        return p

    def run_gipps_simulation_with_braking(self,
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