def reward(microgrid, purchased_cost):
    S = microgrid.SoldBackReward()
    O = microgrid.OperationalCost()

    return S - O - purchased_cost
