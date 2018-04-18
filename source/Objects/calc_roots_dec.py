def cal_dec(car):
    comf_dec = -0.54
    if not car.leader:
        return comf_dec  # comfort deceleration
    vl0 = car.leader.v
    v0 = car.v
    alm = car.leader.comf_dec
    ap = car.a
    tr = car.max_braking_response_time

    def calc_am(tb):
        am = (vl0 + alm * tr + alm * tb - v0 - ap * tr) / tb
        return am

    vl1 = vl0 + alm * tr
    v1 = v0 + ap * tr

    dx0 = car.leader.loc - car.loc - car.leader.length
    dx1 = dx0 + vl0 * tr + 0.5 * alm * tr * tr - (v0 * tr + 0.5 * ap * tr * tr)
    dx2 = dx1
