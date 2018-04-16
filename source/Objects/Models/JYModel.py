from Objects.Models.CAVModel import CAVModel


class JYModel:
    def __init__(self):
        self.cavmodel = CAVModel()

    def denominator(self, car, dt):
        pcar = car.leader
        clr = pcar.loc - car.loc - pcar.length  # clearance of the vehicle
        deno = clr + pcar.v * dt + pcar.a * dt * dt / 2 - car.v * dt - car.h * car.v
        return deno

    def numerator(self, car, dt):
        numer = dt * car.h + dt * dt / 2
        return numer

    def get_acc(self, car):
        if not car.leader:
            return car.comf_acc
        if not car.connected:
            return self.cavmodel.get_acc(car)
        dt = car.simulationStep / 1000
        deno = self.denominator(car, dt)
        numer = self.numerator(car, dt)
        acc = deno / numer
        acc = max(min(a, car.max_acc), car.max_dec)
        time = car.simulationStep / 1000
        if car.maxBraking:
            new_a = car.max_dec
        elif car.braking_signal:
            new_a = car.comf_dec
        else:
            new_a = acc
        new_v = car.v + new_a * time
        if new_v < 0:
            new_v = 0
            new_a = (new_v - car.v) / time
        return new_a