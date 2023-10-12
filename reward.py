def reward(microgrid, purchased_cost):
    S = microgrid.SoldBackReward()
    O = microgrid.operational_cost()

    return S - O - purchased_cost
