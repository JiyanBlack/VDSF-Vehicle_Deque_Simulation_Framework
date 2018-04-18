class JYModel:
    def denominator(self, car, dt):
        pcar = car.leader
        clr = pcar.loc - car.loc - pcar.length  # clearance of the vehicle
        deno = clr + pcar.v * dt + pcar.a * dt * dt / 2 - car.v * dt - car.h * car.v
        return deno

    def numerator(self, car, dt):
        numer = dt * car.h + dt * dt / 2
        return numer

    def get_acc(self, car):
        if not car.leader or car.v == 0:
            return car.comf_acc
        h = (car.leader.loc - car.loc) / car.v
        if h <= car.h:
            dt = car.simulationStep / 1000
            deno = self.denominator(car, dt)
            numer = self.numerator(car, dt)
            acc = deno / numer
            acc = max(min(acc, car.max_acc), car.max_dec)
            return acc
        return car.comf_acc

    def get_new_v(self, car):
        time = car.simulationStep / 1000
        if car.braking_timestamp > 0:
            if car.braking_timestamp < car.simTime:
                new_a = car.a_at_signal
            else:
                new_a = car.comf_dec
        else:
            new_a = self.get_acc(car)
        new_v = car.v + new_a * time
        if new_v < 0:
            new_v = 0
        return new_v
