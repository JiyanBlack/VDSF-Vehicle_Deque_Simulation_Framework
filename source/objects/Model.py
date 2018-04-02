class CAVModel:
    def __init__(self):
        self.k = 0.3  # constant-speed error factor
        self.ka = 1.0  # constant factor in eq3
        self.kv = 0.58  # constant factor in eq3
        self.kd = 0.1  # constant factor in eq3

    def get_aref_v(self, car):
        '''
        get aref_v according to eq2
        '''
        return self.k * (car.v_intend - car.v)

    def get_r_ref(self, car, pcar):
        '''
        get r_ref according to eq4
        '''
        rsafe = (car.v**2) / 2 * ((1 / pcar.max_dec) - (1 / car.max_dec))
        rsys = car.tsys * car.v
        rref = max(rsafe, rsys, car.miniGap)
        return rref

    def get_aref_d(self, car, pcar):
        '''
        get aref_d according to eq3
        '''
        r = pcar.loc - car.loc  # clearance of the vehicle
        rref = self.get_r_ref(car, pcar)
        return self.ka * pcar.a + self.kv * (pcar.v - car.v) + self.kd * (
            r - rref)

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
        return acc