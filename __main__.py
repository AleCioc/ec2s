import datetime

import numpy as np
import pandas as pd

from load_data import get_input_data
from geo_preprocessing import get_gdfs
from get_traceB_input import get_traceB_input
from get_eventG_input import get_eventG_input
from run_traceB_sim import run_traceB_sim
from run_eventG_sim import run_eventG_sim
from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Init general conf and data structure
"""

city = "Torino"
bin_side_length = 500

sim_general_conf = {

    "city": city,
    "bin_side_length": bin_side_length,
    "requests_rate_factor": 1,
    "n_cars": 400,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 10, 8)
}

#months = [9]

#bookings,\
#parkings,\
#grid,\
#bookings_origins_gdf,\
#bookings_destinations_gdf,\
#parkings_gdf = get_input_data(city, months, bin_side_length)

bookings = pd.read_pickle("./Data/" + city + "_bookings.pickle")
grid = pd.read_pickle("./Data/" + city + "_grid.pickle")

#fig, ax = plt.subplots(1, 1)
#grid.plot(color='white', edgecolor='black', ax=ax)
#grid.geometry.iloc[300:302].plot(ax=ax)

sim_scenario_conf = {

    "time_estimation": True,
    "queuing": True,
    "beta": 100,

    "hub": True,
    "hub_zone_policy": "default",
    "hub_zone": 300,
    "hub_n_charging_poles": 50,
    "relocation": False,
    "finite_workers": False,
    
    "distributed_cps": False,
    "cps_placement_policy": "default",
    "n_charging_poles": 50,
    "cps_zones_percentage": 0.1,
    
    "user_contribution": False,
    "willingness": 0.99,    
    
    }

simInput_eventG = get_eventG_input\
    (sim_general_conf,
     sim_scenario_conf, 
     grid,
     bookings)

sim_eventG = run_eventG_sim\
    (simInput = simInput_eventG)        

simOutput_eventG = EFFCS_SimOutput(sim_eventG)
print (simOutput_eventG.sim_stats)
#print (simOutput_eventG.sim_stats.loc["n_no_close_cars"])
#print (simOutput_eventG.sim_stats.loc["n_deaths"])

"""
Only hub, no users contribution, no time estimation
Varying:
    Queuing / No Queuing
    Hub capacity
    Beta
"""

#sim_stats_df = pd.DataFrame()
#
#sim_scenario_conf = {
#
#    "time_estimation": False,
#    "queuing": True,
#    "beta": 100,
#
#    "hub": True,
#    "hub_zone_policy": "default",
#    "hub_zone": 0,
#    "hub_n_charging_poles": 20,
#    "relocation": False,
#    "finite_workers": False,
#    
#    "distributed_cps": True,
#    "cps_placement_policy": "default",
#    "n_charging_poles": 50,
#    "cps_zones_percentage": 0.1,
#    
#    "user_contribution": False,
#    "willingness": 0.99,    
#    
#    }
#
#for queuing in [True, False]:
#    for hub_n_charging_poles in np.arange(20, 101, 5):
#        for beta in np.arange(40, 101, 5):
#            
#            print (queuing,
#                   hub_n_charging_poles,
#                   beta)
#            
#            sim_scenario_conf["queuing"]\
#                = queuing
#            sim_scenario_conf["hub_n_charging_poles"]\
#                = hub_n_charging_poles
#            sim_scenario_conf["beta"]\
#                = beta
#            
#            simInput_eventG = get_eventG_input\
#                (sim_general_conf,
#                 sim_scenario_conf, 
#                 grid,
#                 bookings)
#            
#            sim_eventG = run_eventG_sim\
#                (simInput = simInput_eventG)        
#    
#            simOutput_eventG = EFFCS_SimOutput(sim_eventG)
##            print (simOutput_eventG.sim_stats)
#
#            sim_stats_df = pd.concat\
#                ([sim_stats_df,
#                  simOutput_eventG.sim_stats], 
#                axis=1, ignore_index=True, sort=False)
#
#sim_stats_df = sim_stats_df.T
#sim_stats_df.to_pickle("only_hub_results.pickle")

"""
Hub + cps, with users contribution, no time estimation
Varying:
    Queuing / No Queuing
    Hub capacity
    Beta
"""

#sim_stats_df = pd.DataFrame()
#
#sim_scenario_conf = {
#
#    "time_estimation": False,
#    "queuing": True,
#    "beta": 100,
#
#    "hub": False,
#    "hub_zone_policy": "default",
#    "hub_zone": 0,
#    "hub_n_charging_poles": 20,
#    "relocation": False,
#    "finite_workers": False,
#    
#    "distributed_cps": True,
#    "cps_placement_policy": "default",
#    "n_charging_poles": 50,
#    "cps_zones_percentage": 0.1,
#    
#    "user_contribution": True,
#    "willingness": 0.99,    
#    
#    }
#
#for queuing in [True]:
#    for n_charging_poles in np.arange(40, 101, 5):
#        for beta in np.arange(40, 45, 5):
#            
#            hub_n_charging_poles = \
#                100 - n_charging_poles
#
#            print (queuing,
#                   hub_n_charging_poles,
#                   n_charging_poles,
#                   beta)
#            
#            sim_scenario_conf["queuing"]\
#                = queuing
#            sim_scenario_conf["hub_n_charging_poles"]\
#                = hub_n_charging_poles
#            sim_scenario_conf["n_charging_poles"]\
#                = n_charging_poles
#            sim_scenario_conf["beta"]\
#                = beta
#            
#            simInput_eventG = get_eventG_input\
#                (sim_general_conf,
#                 sim_scenario_conf, 
#                 grid,
#                 bookings)
#            
#            sim_eventG = run_eventG_sim\
#                (simInput = simInput_eventG)        
#    
#            simOutput_eventG = EFFCS_SimOutput(sim_eventG)
##            print (simOutput_eventG.sim_stats)
#
#            sim_stats_df = pd.concat\
#                ([sim_stats_df,
#                  simOutput_eventG.sim_stats], 
#                axis=1, ignore_index=True, sort=False)
#
#sim_stats_df = sim_stats_df.T
#sim_stats_df.to_pickle("hub_and_cps_results.pickle")

"""
Only distributed cps, no time estimation
Varying:
    Users contribution / No Users contribution
    Queuing / No Queuing
    Hub capacity
    Beta
"""

#sim_stats_df = pd.DataFrame()
#
#sim_scenario_conf = {
#
#    "time_estimation": False,
#    "queuing": True,
#    "beta": 100,
#
#    "hub": False,
#    "hub_zone_policy": "default",
#    "hub_zone": 0,
#    "hub_n_charging_poles": 20,
#    "relocation": False,
#    "finite_workers": False,
#    
#    "distributed_cps": True,
#    "cps_placement_policy": "default",
#    "n_charging_poles": 50,
#    "cps_zones_percentage": 0.1,
#    
#    "user_contribution": False,
#    "willingness": 0.99,    
#    
#    }
#
#for queuing in [True]:
#    for n_charging_poles in np.arange(40, 101, 5):
#        for beta in np.arange(40, 101, 5):
#            for user_contribution in [True, False]:
#
#                print (queuing,
#                       n_charging_poles,
#                       beta,
#                       user_contribution)
#                
#                sim_scenario_conf["queuing"]\
#                    = queuing
#                sim_scenario_conf["n_charging_poles"]\
#                    = n_charging_poles
#                sim_scenario_conf["beta"]\
#                    = beta
#                sim_scenario_conf["user_contribution"]\
#                    = user_contribution
#                
#                simInput_eventG = get_eventG_input\
#                    (sim_general_conf,
#                     sim_scenario_conf, 
#                     grid,
#                     bookings)
#                
#                sim_eventG = run_eventG_sim\
#                    (simInput = simInput_eventG)        
#        
#                simOutput_eventG = EFFCS_SimOutput(sim_eventG)
##                print (simOutput_eventG.sim_stats)
#    
#                sim_stats_df = pd.concat\
#                    ([sim_stats_df,
#                      simOutput_eventG.sim_stats], 
#                    axis=1, ignore_index=True, sort=False)
#
#sim_stats_df = sim_stats_df.T
#sim_stats_df.to_pickle("only_cps_results.pickle")
