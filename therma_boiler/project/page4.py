import CoolProp.CoolProp as CP

# Calculation functions
def energy_input_from_fuel(mfuel, hL, Cpf, X_h, tf, td, ta, mairwet, msteam, Hs):
    Hf = Cpf * (tf - td)
    H_fuel = (hL + Hf) * mfuel
    MWair = (1 - X_h) * 28.84 + X_h * 18
    Mair = mairwet / MWair
    Cpair = 33.915 + 1.214e-3 * (ta + td) / 2
    Cphum = 34.42 + 6.281e-4 * (ta + td) / 2 + 5.6106e-6 * pow(((ta + td) / 2), 2)
    Ha = ((1 - X_h) * Cpair + X_h * Cphum) * (ta - td) * Mair
    Hm = msteam * Hs
    return H_fuel + Ha + Hm

def Energy_Output(mfuel, hL, radiation_loss, tg, td, xc, m3, xo, xn, xh, xs, Q_in):
    Cpco2 = 43.2936 + 0.0115 * (tg + td) / 2 - 818558.5 / pow(((tg + td) / 2), 2)
    Nco2 = xc * m3 / 44
    Hco2 = Nco2 * Cpco2 * (tg - td)
    Cpo2 = 34.627 + 1.0802e-3 * (tg + td) / 2 - 785900 / pow(((tg + td) / 2), 2)
    No2 = xo * m3 / 32
    Ho2 = No2 * Cpo2 * (tg - td)
    Cpn2 = 27.2155 + 4.187e-3 * (tg + td) / 2
    Nn2 = xn * m3 / 28
    Hn2 = Nn2 * Cpn2 * (tg - td)
    Cph2o = 34.417 + 6.281e-4 * (tg + td) / 2 - 5.611e-6 * pow(((tg + td) / 2), 2)
    Nh2o = xh * m3 / 18
    Hh2o = Nh2o * Cph2o * (tg - td)
    Cpso2 = 32.24 + 0.0222 * (tg + td) / 2 - 3.475e-5 * pow(((tg + td) / 2), 2)
    Nhso2 = xs * m3 / 64
    Hso2 = Nhso2 * Cpso2 * (tg - td)
    hs = Hco2 + Ho2 + Hn2 + Hh2o + Hso2
    hr = radiation_loss * hL * mfuel
    Q_out = hs + hr
    Qu = Q_in - Q_out
    return Qu

def efficiency_by_direct_method_Net(Qu, Q_in):
    return 100 * (Qu / Q_in)

def efficiency_by_direct_method_Gross(Qu, Q_in, hL, X_h):
    hH = hL + X_h * 2464.9
    return 100 * (Qu / (Q_in - hL + hH))

def efficiency_by_direct_method_Fuel(Qu, mfuel, hL):
    return 100 * (Qu / (hL * mfuel))

