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

class environment(gym.Env):
    def __init__(self, microgrid = Microgrid()):
        self.microgrid = microgrid
        self.action_space = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.observation_space = np.array([0,0,0,0])
        self._curr_step = 0
        self._curr_ep = 0

    def reset(self):
        self.microgrid = Microgrid()
        self.action_space = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.observation_space = np.array([0,0,0,0])
        self._curr_step = 0
        self._curr_episode = 0

        obs = np.array([solarirradiance[self._curr_step], windspeed[self._curr_step], rate_consumption_charge[self._curr_step], self.microgrid.SOC])
        return obs
        
        

    def step(self, actions):
        print(f"Current step :{self._curr_step}. Current episode: {self._curr_ep}", end = "\r")

        self._curr_step += 1

        term = False
        trunc = False

        if self._curr_step == len(windspeed)-1:
            term = True
            self._curr_ep += 1
            print("", end = "\n")

        self.microgrid.actions_adjustingstatus = actions[0:3]
        self.microgrid.actions_solar = actions[3:6]
        self.microgrid.actions_wind = actions[6:9]
        self.microgrid.actions_generator = actions[9:12]
        self.microgrid.actions_purchased = actions[12:14]
        self.microgrid.actions_discharged = actions[14]

        self.microgrid.transition()

        obs = np.array([solarirradiance[self._curr_step], windspeed[self._curr_step], rate_consumption_charge[self._curr_step], self.microgrid.SOC])
        r = reward(self.microgrid, actions[12:14]*rate_consumption_charge[self._curr_step])

        return obs, r, term, trunc

    def render(self, mode = "human"):
        """
            Matplotlib stuff or smth
            not sure what the render would be
        """
        ...
    def seed(self, sd):
        self.sd = sd
