from math import sqrt
from math import exp

class GippsModel:
    '''
    Original Gipps Model from Gipps, P. G. "A behavioural car-following model for computer simulation"
    '''

    def __init__(self):
        self.ag = 0.6
        self.l1 = 50 / 3
        self.l2 = 10 / 3

    
    def get_g(self, car):
        '''
        Get a desired speed factor - g to reduce desired speed at junctions,
        see:Simulation using gipps’ car-following model—an in-depth analysis
        '''
        x1 = max(0 - car.loc, 0)
        x2 = max(car.loc - 0, 0)
        inside_exp = -(x1**2) / (2 * (self.l1 ** 2)) - (x2 ** 2) / (2 * (self.l2 ** 2))
        g = 1 - self.ag * exp(inside_exp)
        return g

    def calc_free_travel(self, car):
        inside_sqrt = (0.025 + car.v / car.vi)
        if inside_sqrt<=0:
            print("free travel error",inside_sqrt, car.v, car.vi)
            # return car.v
        return car.v + 2.5 * car.an * car.tn * (1 - car.v / car.vi) * sqrt(inside_sqrt)

    def calc_car_following(self, car):
        inside_sqrt = (car.bn**2) * (car.tn**2) - car.bn * (
            2 * (car.leader.loc - car.leader.sn - car.loc) - car.v * car.tn -
            (car.leader.v**2) / car.b_hat)
        if inside_sqrt <= 0:
            print("carfollowing error", inside_sqrt, car.v, car.vi)
            # return car.bn * car.tn
        return car.bn * car.tn  + sqrt(inside_sqrt)

    def get_speed(self, car):
        g = self.get_g(car)
        car.vi = g * car.max_v
        v2 = self.calc_free_travel(car)
        if car.leader:
            v8 = self.calc_car_following(car)
            return min(v2, v8)
        return v2


class GippsCongestModel:
    '''
    Original Gipps Model from Gipps, P. G. "A behavioural car-following model for computer simulation"
    '''

    def __init__(self):
        self.Dn = 0

    def calc_free_travel(self, car):
        return car.v + 2.5 * car.an * car.tn * (1 - car.v / car.vi) * ((0.025 + car.v / car.vi)**0.5)

    def calc_car_following(self, car):
        inside_sqrt = (car.bn ** 2) * (car.tn**2)/4 - car.bn * (2 * (car.leader.loc - car.leader.sn - car.loc) - car.v * car.tn - (car.leader.v ** 2)/car.leader.bn + self.Dn)
        before_sqrt = car.bn * car.tn/2
        return before_sqrt + sqrt(inside_sqrt)

    def get_speed(self, car):
        v_free = self.calc_free_travel(car)
        if not car.leader:
            return v_free
        v_follow = self.calc_car_following(car)
        return min(v_free, v_follow)