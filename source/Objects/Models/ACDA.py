class ACDAModel:
    '''
    Autonomous Vehicle driving model according to ACDA criteria:
    See paper: 
    "Automated cars: Queue discharge at signalized intersections with 'Assured-Clear-Distance-Ahead' driving strategies"
    '''
    def __init__(self):
        self.t_lag_plus = 0.2
        self.t_lag_minus = 0.4
        self.k = 0.1  # constant-speed error factor
        self.ka = 1.0  # constant factor in eq3
        self.kv = 0.58  # constant factor in eq3
        self.kd = 0.1  # constant factor in eq3
        self.default_tsys = 1.4

    def get_mini_spacing(self, car):
        xf = car.v * self.t_lag_minus + 1/2 * (car.v**2)/ car.max_dec
        xl = 1/2 * (car.leader.v ** 2) / car.leader.max_dec
        xmin = xf - xl
        return xmin

    def get_aref_v(self, car):
        '''
        get aref_v according to eq2
        '''
        return self.k * (car.vi - car.v)

    def get_r_ref(self, car, pcar):
        '''
        get r_ref according to eq4
        '''
        rsafe = (car.v**2) / 2 * ((1 / pcar.max_dec) - (1 / car.max_dec))
        rsys = car.v * self.default_tsys
        rmin = car.miniGap
        rref = max(rsafe, rsys, rmin)
        return rref

    def get_aref_d(self, car, pcar):
        '''
        get aref_d according to eq3
        '''
        r = pcar.loc - car.loc - pcar.length  # clearance of the vehicle
        rref = self.get_r_ref(car, pcar)
        xmin = self.get_mini_spacing(car)
        if car.v > 0 and rref < xmin:
            rref = xmin
        return self.ka * pcar.a + self.kv * (pcar.v - car.v) + self.kd * (r - rref)

    def get_acc(self, car):
        '''
        Get acceleration of the vehicle 
        '''
        aref_v = self.get_aref_v(car)
        pcar = car.leader
        if pcar:
            aref_d = self.get_aref_d(car, pcar)
            acc = min(aref_v, aref_d)
        else:
            acc = aref_v
        acc = max(min(acc, car.max_acc), car.max_dec)
        if not car.start_timestamp: 
            if pcar:
                if pcar.start_timestamp:
                    time_diff = (car.simTime - pcar.start_timestamp) / 1000
                    if time_diff <= self.t_lag_plus:
                        acc = 0
                    else:
                        car.start_timestamp = car.simTime
                else:
                    acc = 0
            else:
                car.start_timestamp = car.simTime
        return acc