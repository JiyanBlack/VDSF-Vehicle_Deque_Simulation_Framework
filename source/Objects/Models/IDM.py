import math

class IDM:
    '''
    IDM model in Modeling Cooperative and Autonomous Adaptive
Cruise Control Dynamic Responses Using Experimental Data
    '''
    def __init__(self):
        self.sigma = 4
        self.T = 1.0

    def get_time_gap(self, car):
        return self.T + car.t_lag_minus
        xf = car.v * car.t_lag_minus + 1/2 * (car.v**2)/ car.max_dec
        xl = 1/2 * (car.leader.v ** 2) / car.leader.max_dec
        xmin = xf - xl + car.leader.length
        if car.v < 1:
            hmin = xmin / car.v
        return hmin

    def get_s_star(self, car):
        s_3 = car.v * (car.v - car.leader.v) / (2 * math.sqrt(abs(car.max_acc * car.max_dec)))
        s_star = car.miniGap + car.v * self.get_time_gap(car) + s_3
        return s_star

    def get_IDM_acc(self,car):
        a_term = 1 - (car.v/car.max_v)**self.sigma
        if car.leader:
            s_star = self.get_s_star(car)
            s = car.leader.loc - car.loc
            a_term -= (s_star/s)**2
        a = car.max_acc * a_term
        return a

    def get_acc(self, car):
        '''
        Get acceleration of the vehicle 
        '''
        acc = self.get_IDM_acc(car)
        pcar = car.leader
        acc = max(min(acc, car.max_acc), car.max_dec)
        if not car.start_timestamp: 
            if pcar:
                if pcar.start_timestamp:
                    time_diff = (car.simTime - pcar.start_timestamp) / 1000
                    if time_diff <= car.t_lag_plus:
                        acc = 0
                    else:
                        car.start_timestamp = car.simTime
                else:
                    acc = 0
            else:
                time_diff = (car.simTime - 0) / 1000
                if time_diff <= car.t_lag_plus:
                    acc = 0
                else:
                    car.start_timestamp = car.simTime
        return acc