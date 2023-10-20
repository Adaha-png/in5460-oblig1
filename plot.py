import matplotlib.pyplot as plt

def plotSolar(production, timeslot):
    plt.title("Solar power generation", fontdict={'size': 16})
    plt.plot(timeslot,production, "r", label = "Solar generated")
    plt.grid()
    plt.xlabel("Timeslot", fontdict={'size': 12,'family': 'serif'})
    plt.ylabel("Solar Generation", fontdict={'size': 12,'family': 'serif'})
    plt.show()

def plotSolarWind(solar_generation, wind_generation, timeslot):
    plt.title("Solar and Wind generation", fontdict={"size":16})
    plt.plot(timeslot,solar_generation, "r", label = "Solar generated")
    plt.plot(timeslot,wind_generation, "b", label="Wind generation")
    plt.grid()
    plt.xlabel("Timeslot", fontdict={'size': 12,'family': 'serif'})
    plt.ylabel("Solar and Wind Generation", fontdict={'size': 12,'family': 'serif'})
    plt.show()

def plotGeneration(solar_generation, wind_generation, generator_generation, timeslot):
    plt.title("Solar and Wind generation", fontdict={"size":16})
    plt.plot(timeslot,solar_generation, "r", label = "Solar generated")
    plt.plot(timeslot,wind_generation, "b", label="Wind generation")
    plt.plot(timeslot,generator_generation, "g", label="Generation generation")
    plt.grid()
    plt.xlabel("Timeslot", fontdict={'size': 12,'family': 'serif'})
    plt.ylabel("Power Generation", fontdict={'size': 12,'family': 'serif'})
    plt.show()