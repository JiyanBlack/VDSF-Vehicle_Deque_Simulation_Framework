class Platoon:
    def __init__(self):
        self.n = 0
        self.platoon = []
        self.records = {}
        self.delays = []
        self.vehPass = 0

    def add_vehicle(self, car):
        self.platoon.append(car)
        self.n += 1

    def run(self, loop_num):
        # run simulation
        for i in range(loop_num):
            for idx in range(self.n):
                self.platoon[idx].update()
        # save all vehicle information to an object
        lastUpdate = sorted(self.platoon[idx].records.keys())[-1]
        for idx in range(self.n):
            idxLoc = self.platoon[idx].records[lastUpdate][2]
            self.records[idx] = self.platoon[idx].records
            self.delays.append(self.platoon[idx].delay)
            if  idxLoc > 0:
                self.vehPass += 1
