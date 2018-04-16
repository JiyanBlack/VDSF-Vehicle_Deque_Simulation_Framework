class CAVModel:
    '''
    CACC Model from paper: The impact of cooperative adaptive cruise control on traffic-flow characteristics by Van Arem, Bart
    Van Driel, Cornelia J.G.
    Visser, Ruben
    '''

    def __init__(self):
        self.k = 0.3  # constant-speed error factor
        self.ka = 1.0  # constant factor in eq3
        self.kv = 0.58  # constant factor in eq3
        self.kd = 0.1  # constant factor in eq3

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
        rsys = car.tsys * car.v
        rmin = car.miniGap
        rref = max(rsafe, rsys, rmin)
        return rref

    def get_aref_d(self, car, pcar):
        '''
        get aref_d according to eq3
        '''
        r = pcar.loc - car.loc - pcar.length  # clearance of the vehicle
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
