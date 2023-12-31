import numpy as np

cutin_windspeed =3*3.6
#the cut -in windspeed (km/h =1/3.6 m/s), v^ci#
cutoff_windspeed =11*3.6
#the cut -off windspeed (km/h =1/3.6 m/s), v^co#
rated_windspeed =7*3.6
#the rated windspeed (km/h =1/3.6 m/s), v^r#
charging_discharging_efficiency =0.95
#the charging - discharging efficiency , eta#
rate_battery_discharge =2/1000
#the rate for discharging the battery ( MegaWatt ), b#
unit_operational_cost_solar =0.15/10
#the unit operational and maintanance cost for generating power
# from solar PV (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^s#
unit_operational_cost_wind =0.085/10
#the unit operational and maintanance cost for generating power
# from wind turbine (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^w#
unit_operational_cost_generator =0.55/10
#the unit opeartional and maintanance cost for generating power
# from generator (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^g#
unit_operational_cost_battery =0.95/10
#the unit operational and maintanance cost for battery storage system
#per unit charging / discharging cycle (10^4 $/ MegaWattHour =10 $/ kWHour ),
# r_omc ^b#
capacity_battery_storage =300/1000
#the capacity of battery storage system ( MegaWatt Hour =1000 kWHour ), e#
SOC_max =0.95* capacity_battery_storage
#the maximum state of charge of battery system #
SOC_min =0.05* capacity_battery_storage
#the minimum state of charge of battery system #
area_solarPV =1400/(1000*1000)
#the area of the solar PV system (km ^2=1000*1000 m^2) , a#
efficiency_solarPV =0.2
#the efficiency of the solar PV system , delta #
density_of_air =1.225
# calculate the rated power of the wind turbine ,
# density of air (10^6 kg/km ^3=1 kg/m^3) , rho#
radius_wind_turbine_blade =25/1000
# calculate the rated power of the wind turbine ,
# radius of the wind turbine blade (km =1000 m), r#
average_wind_speed =3.952*3.6
# calculate the rated power of the wind turbine ,
# average wind speed (km/h =1/3.6 m/s), v_avg ( from the windspeed table )#
power_coefficient =0.593
# calculate the rated power of the wind turbine , power coefficient , theta #
gearbox_transmission_efficiency =0.95
# calculate the rated power of the wind turbine ,
# gearbox transmission efficiency , eta_t #
electrical_generator_efficiency =0.95
# calculate the rated power of the wind turbine ,
# electrical generator efficiency , eta_g #
rated_power_wind_turbine_original =0.5* density_of_air * np . pi * radius_wind_turbine_blade * radius_wind_turbine_blade * average_wind_speed * average_wind_speed * average_wind_speed * power_coefficient * gearbox_transmission_efficiency * electrical_generator_efficiency

rated_power_wind_turbine = rated_power_wind_turbine_original /(3.6*3.6*3.6)
#the rated power of the wind turbine , RP_w ( MegaWatt =10^6 W),
# with the radius_wind_turbine_blade measured in km =10^3m,
# average wind speed measured in km/ hour =3.6 m/s,
# RP_w will be calculated as RP_w_numerical
# then RP_w in MegaWatt =(1 kg/m^3) *(10^3 m) *(10^3 m)
# *(3.6 m/s) *(3.6 m/s) *(3.6 m/s)* RP_w_numerical
# =3.6^3*10^6 RP_w_numerical W =3.6^3 RP_w_numerical MegaWatt #
number_windturbine =1
#the number of wind turbine in the onsite generation system , N_w#
number_generators =1
#the number of generators , n_g#
rated_output_power_generator =600/1000
#the rated output power of the generator ( MegaWatt =1000 kW), G_p#

unit_reward_soldbackenergy = 0.2
Delta_t = 1
class Microgrid(object):
    def __init__(self,
            solar,
            wind,
            generator,
            workingstatus =[0 ,0 ,0], #the working status of [ solar PV , wind turbine , generator]
            SOC =0, #the state of charge of the battery system
            actions_adjustingstatus =[0 ,0 ,0], #the actions of adjusting the working status ( connected=1 or not =0 to the load ) of the [solar , wind , generator ]
            actions_solar =[0 ,0 ,0], #the solar energy used for supporting [the energy load , charging battery , sold back ]
            actions_wind =[0 ,0 ,0], #the wind energy used for supporting [the energy load , charging battery , sold back ]
            actions_generator =[0 ,0 ,0], #the use of the energy generated by the generator for supporting [the energy load , charging battery , sold back ]
            actions_purchased =[0 ,0], #the use of the energy purchased from the grid for supporting [the energy load , charging battery ]
            actions_discharged =0, #the energy discharged by the battery for supporting the energy load
            solarirradiance =0, #the environment feature : solar irradiance at current decision epoch
            windspeed =0 #the environment feature : wind speed at current decision epoch
    ):
        self.workingstatus = workingstatus
        self.SOC = SOC
        self.actions_adjustingstatus = actions_adjustingstatus
        self.actions_solar = actions_solar
        self.actions_wind = actions_wind
        self.actions_generator = actions_generator
        self.actions_purchased = actions_purchased
        self.actions_discharged = actions_discharged
        self.solarirradiance = solarirradiance
        self.windspeed = windspeed
        self.solarLog = []
        self.windLog = []
        self.generatorLog = []
        self.wind = wind
        self.solar = solar
        self.generator = generator

    def transition(self):
        self.solarLog.append(self.energy_generated_solar())
        self.windLog.append(self.energy_generated_wind())
        self.generatorLog.append(self.energy_generated_generator())
        workingstatus = self.workingstatus
        SOC = self.SOC

        if self.actions_adjustingstatus[0]==1:
            workingstatus[0]=self.solar
        else:
            workingstatus[0]=0
            # determining the next decision epoch working status of solar PV , 1= working , 0= not working
        if self.actions_adjustingstatus[1]==0 or self.windspeed > cutoff_windspeed or self.windspeed < cutin_windspeed :
            workingstatus[1]=0
        else :
            if self.actions_adjustingstatus[1]==1 and self.windspeed <= cutoff_windspeed and self.windspeed >= cutin_windspeed :
                workingstatus[1]=self.wind
            # determining the next decision epoch working status of wind turbine , 1= working , 0= not working

        if self.actions_adjustingstatus[2]==1:
            workingstatus[2]=self.generator
        else:
            workingstatus[2]=0
            #determining the next decision epoch working status of generator , 1= working , 0= not working
            SOC = self.SOC +( self.actions_solar[1]*self.energy_generated_solar()+ self.actions_wind[1]*self.energy_generated_wind()+ self.actions_generator[1]*self.energy_generated_generator()+ self.actions_purchased[1]) * charging_discharging_efficiency - self.actions_discharged / charging_discharging_efficiency

        if SOC > SOC_max:
            SOC = SOC_max

        if SOC < SOC_min:
            SOC = SOC_min
            # determining the next desicion epoch SOC , state of charge of the battery system
        return workingstatus , SOC

    def EnergyConsumption(self):
        # returns the energy consumption from the grid
        return -(self.actions_solar[0]*self.energy_generated_solar()+self.actions_wind[0]*self.energy_generated_wind()+self.actions_generator[0]*self.energy_generated_generator()+self.actions_discharged)

    def energy_generated_solar(self):
        # calculate the energy generated by the solar PV , e_t^s#
        if self.workingstatus [0]==1:
            energy_generated_solar = self.solarirradiance * area_solarPV * efficiency_solarPV /1000

        else:
            energy_generated_solar = 0

        return energy_generated_solar

    def energy_generated_wind ( self ) :
        # calculate the energy generated by the wind turbine , e_t^w#
        if self.workingstatus[1]==1 and self.windspeed < rated_windspeed and self.windspeed >= cutin_windspeed :
            energy_generated_wind = number_windturbine * rated_power_wind_turbine *( self.windspeed - cutin_windspeed ) /( rated_windspeed - cutin_windspeed )
        else:
            if self.workingstatus[1]==1 and self.windspeed < cutoff_windspeed and self.windspeed >= rated_windspeed :
                energy_generated_wind = number_windturbine * rated_power_wind_turbine * Delta_t
            else:
                energy_generated_wind =0

        return energy_generated_wind

    def energy_generated_generator ( self ) :
        # calculate the energy generated bv the generator , e_t^g#
        if self.workingstatus[2] == 1:
            energy_generated_generator = number_generators * rated_output_power_generator * Delta_t
        else:
            energy_generated_generator = 0

        return energy_generated_generator

    def OperationalCost(self):
        # returns the operational cost for the onsite generation system #
        if self.workingstatus[0]==1:
            energy_generated_solar = self.solarirradiance * area_solarPV * efficiency_solarPV /1000
        else:
            energy_generated_solar =0
            # calculate the energy generated by the solar PV , e_t^s#

        if self.workingstatus[1]==1 and self.windspeed < rated_windspeed and self.windspeed >= cutin_windspeed :
            energy_generated_wind = number_windturbine * rated_power_wind_turbine * (self.windspeed - cutin_windspeed) / (rated_windspeed - cutin_windspeed)
        else:
            if self.workingstatus[1]==1 and self.windspeed < cutoff_windspeed and self.windspeed >= rated_windspeed:
                energy_generated_wind = number_windturbine * rated_power_wind_turbine * Delta_t
            else:
                energy_generated_wind =0

            # calculate the energy generated by the wind turbine , e_t^w#
        if self.workingstatus[2]==1:
            energy_generated_generator = number_generators * rated_output_power_generator * Delta_t
        else:
            energy_generated_generator =0
            # calculate the energy generated bv the generator , e_t^g#
        operational_cost = energy_generated_solar * unit_operational_cost_solar + energy_generated_wind * unit_operational_cost_wind + energy_generated_generator * unit_operational_cost_generator

        operational_cost += (self.actions_discharged + self.actions_solar[1] + self.actions_wind[1] + self.actions_generator[1]) * Delta_t * unit_operational_cost_battery / (2 * capacity_battery_storage * (SOC_max-SOC_min))
        # calculate the operational cost for the onsite generation system
        return operational_cost

    def SoldBackReward(self):
        # calculate the sold back reward ( benefit )#
        return (self.actions_solar[2]*self.energy_generated_solar() + self.actions_wind[2]*self.energy_generated_wind()+ self.actions_generator[2]*self.energy_generated_generator()) * unit_reward_soldbackenergy

    def PrintMicrogrid ( self , file ) :
        # print the current and the next states of the microgrid #
        print (" Microgrid working status [ solar PV , wind turbine , generator ]=", self.workingstatus , ", SOC =", self.SOC , file = file )
        print (" microgrid actions [ solar PV , wind turbine , generator ]=", self.actions_adjustingstatus , file = file )
        print (" solar energy supporting [the energy load , charging battery, sold back ]=", self.actions_solar , file = file )
        print (" wind energy supporting [the energy load , charging battery , sold back ]=", self.actions_wind , file = file )
        print (" generator energy supporting [the energy load , charging battery , sold back ]=", self.actions_generator , file = file )
        print (" energy purchased from grid supporting [the energy load , charging battery ]=", self.actions_purchased , file = file )
        print (" energy discharged by the battery supporting the energy load =", self.actions_discharged , file = file )
        print (" solar irradiance =", self.solarirradiance , file = file )
        print (" wind speed =", self.windspeed , file = file )
        print (" Microgrid Energy Consumption =", self.EnergyConsumption () , file = file )
        print (" Microgrid Operational Cost =", self.OperationalCost () , file = file )
        print (" Microgrid SoldBackReward =", self.SoldBackReward () , file = file )
        print ("\n", file = file )

        return None
