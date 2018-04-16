class Platoon:
    def __init__(self):
        self.n = 0
        self.platoon = []
        self.records = {}

    def add_vehicle(self, car):
        if self.n > 0:
            car.set_leader(self.platoon[self.n - 1])
        self.platoon.append(car)
        self.n += 1

    def run(self, loop_num):
        # run simulation
        for i in range(loop_num):
            for idx in range(self.n):
                self.platoon[idx].update()
        # save all vehicle information to an object
        for idx in range(self.n):
            self.records[idx] = self.platoon[idx].records
