from math import sqrt


class GippsModel:
    '''
    Original Gipps Model from Gipps, P. G. "A behavioural car-following model for computer simulation"
    '''

    def __init__(self):
        pass

    def calc_equation2(self, car):
        return car.v + 2.5 * car.an * car.tn * (1 - car.v / car.vi) * sqrt(
            (0.025 + car.v / car.vi))

    def calc_equation8(self, car):
        inside_sqrt = (car.bn**2) * (car.tn**2) - car.bn * (
            2 * (car.leader.loc - car.leader.sn - car.loc) - car.v * car.tn -
            (car.leader.v**2) / car.b_hat)
        if inside_sqrt > 0:
            return car.bn * car.tn + sqrt(inside_sqrt)
        return car.bn * car.tn

    def get_speed(self, car):
        v2 = self.calc_equation2(car)
        if car.leader:
            v8 = self.calc_equation8(car)
            return min(v2, v8)
        return v2
