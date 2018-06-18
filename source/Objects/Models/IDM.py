import math

class IDM:
    '''
    IDM model in Modeling Cooperative and Autonomous Adaptive
Cruise Control Dynamic Responses Using Experimental Data
    '''
    def __init__(self):
        self.sigma = 4

    def get_s_star(self, car):
        s_3 = car.v * (car.v - car.leader.v) / (2 * math.sqrt(abs(car.max_acc * car.max_dec)))
        s_star = car.miniGap + car.v * car.T + s_3
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
        acc = max(min(acc, car.max_acc), car.max_dec)
        return acc
        # if not car.start_timestamp: 
        #     if pcar:
        #         if pcar.start_timestamp:
        #             time_diff = (car.simTime - pcar.start_timestamp) / 1000
        #             if time_diff <= car.t_lag_plus:
        #                 acc = 0
        #             else:
        #                 car.start_timestamp = car.simTime
        #         else:
        #             acc = 0
        #     else:
        #         time_diff = (car.simTime - 0) / 1000
        #         if time_diff <= car.t_lag_plus:
        #             acc = 0
        #         else:
        #             car.start_timestamp = car.simTime
        # return acc