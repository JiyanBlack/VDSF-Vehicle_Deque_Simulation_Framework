class ACDAModel:
    '''
    Autonomous Vehicle driving model according to ACDA criteria:
    See paper: 
    "Automated cars: Queue discharge at signalized intersections with 'Assured-Clear-Distance-Ahead' driving strategies"
    '''
    def __init__(self):
        self.t_lag_plus = 0.2
        self.t_lag_minus = 0.4
        self.gap = None
        self.ka = 1.0  # constant factor in eq3
        self.kv = 0.58  # constant factor in eq3
        self.kd = 0.1  # constant factor in eq3

    def free_acc(self,car):
        a = -0.4 * (car.v - car.max_v)
        return max(min(a, car.max_acc), car.max_dec)

    def following_acc(self, car):
        xf = car.v * self.t_lag_minus + 1/2 * (car.v**2)/ car.max_dec
        xl = 1/2 * (car.leader.v ** 2) / car.leader.max_dec
        xmin = xf - xl + car.leader.length
        cur_x = car.leader.loc - car.loc
        se = cur_x - xmin
        asc = self.free_acc(car)
        prev_spacing = car.leader.prev_loc - car.prev_loc - car.leader.length
        now_spacing = car.leader.loc - car.loc - car.leader.length
        s_hat = (now_spacing - prev_spacing)/car.gap
        a = s_hat + 0.25 * se
        return max(min(a, asc), car.max_dec)

    def get_acc(self,car):
        self.gap = car.simulationStep / 1000
        if not car.leader:
            acc = self.free_acc(car)
        else:
            acc = self.following_acc(car)
        return max(min(acc, car.max_acc), car.max_dec)