def reward(microgrid, purchased_cost, load, load_purchased):
    S = microgrid.SoldBackReward()
    O = microgrid.OperationalCost()

    load_penalty = 0
    if load+microgrid.EnergyConsumption()-load_purchased>0:
        load_penalty = load+microgrid.EnergyConsumption()-load_purchased 
    return S - O - purchased_cost - load_penalty
