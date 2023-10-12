import numpy as np

import pandas as pd

from reward import reward
from agent import Microgrid


import gym

# read the solar irradiance and wind speed data from file #
# read the rate of consumption charge date from file #
file_SolarIrradiance = "SolarIrradiance.csv"
file_WindSpeed = "WindSpeed.csv"
file_rateConsumptionCharge = "rate_consumption_charge.csv"
# read the solar irradiace
data_solar = pd.read_csv(file_SolarIrradiance)
solarirradiance = np.array(data_solar.iloc[:,3])
# solar irradiance measured by MegaWatt /km ^2
# read the windspeed
data_wind = pd.read_csv(file_WindSpeed)
windspeed = 3.6*np.array(data_wind.iloc[:,3])
# windspeed measured by km/h =1/3.6 m/s
# read the rate of consumption charge
data_rate_consumption_charge = pd.read_csv(file_rateConsumptionCharge)
rate_consumption_charge = np.array(data_rate_consumption_charge.iloc[:,4])/10
# rate of consumption charge measured by 10^4 $/ MegaWatt =10 $/kWh

class env(gym.env):
    def __init__(self, microgrid = Microgrid()):
        super.__init__(self)
        self.microgrid = microgrid
        self.action_space = {
            "adjustingstatus": [0,0,0],
            "solar": [0,0,0],
            "wind": [0,0,0],
            "generator": [0,0,0],
            "purchased": [0,0],
            "discharged": 0
        }
        self.observation_space = [0,0,0,0]
        self._curr_step = 0
        self._curr_ep = 0

    def reset(self):
        self.microgrid = Microgrid()
        self.action_space = {
            "adjustingstatus": [0,0,0],
            "solar": [0,0,0],
            "wind": [0,0,0],
            "generator": [0,0,0],
            "purchased": [0,0],
            "discharged": 0
        }
        self.observation_space = [0,0,0,0]
        self._curr_step = 0
        self._curr_episode = 0

    def step(self, actions):
        print(f"Current step :{self._curr_step}. Current episode: {self._curr_ep}", end = "\r")

        self._curr_step += 1

        term = False
        trunc = False

        if self._curr_step == len(windspeed)-1:
            term = True
            self._curr_ep += 1
            print("", end = "\n")

        microgrid.actions_adjustingstatus = actions["adjustingstatus"]
        microgrid.actions_solar = actions["solar"]
        microgrid.actions_wind = actions["wind"]
        microgrid.actions_generator = actions["generator"]
        microgrid.actions_purchased = actions["purchased"]
        microgrid.actions_discharged = actions["discharged"]

        microgrid.transition()

        obs = np.array([solarirradiance[self._curr_step], windspeed[self._curr_step], rate_consumption_charge[self._curr_step], microgrid.SOC])
        r = reward(self.microgrid, actions["purchased"]*rate_consumption_charge[self._curr_step])

        return obs, r, term, trunc

    def render(self, mode = "human"):
        """
            Matplotlib stuff or smth
            not sure what the render would be
        """
        ...
