import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from DataStructures.City import City

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_traceB_sim import run_traceB_sim
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Init general conf and data structure
"""

city_name = "Torino"
bin_side_length = 500

sim_general_conf = {

    "city": city_name,
    "bin_side_length": bin_side_length,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 11, 1)

}

"""
Set scenario configuration
"""

sim_scenario_conf = {

    "requests_rate_factor": 1,
    "n_cars_factor": 1,

    "time_estimation": False,
    "queuing": True,
    "alpha": 25,
    "beta": 100,

    "hub": True,
    "hub_zone_policy": "num_parkings",
    "hub_n_charging_poles": 20,
    
    "relocation": False,
    "finite_workers": False,
    
    "distributed_cps": False,
    "cps_placement_policy": "num_parkings",
    "n_charging_poles": 20,
    "cps_zones_percentage": 0.1,
    
    "user_contribution": False,
    "system_cps": False,
    "willingness": 0.99,    
    
}

"""
Single Run
"""

# bookings, grid = read_sim_input_data(city_name)

city_obj = City\
    (city_name,
     sim_general_conf)

simInput_eventG = get_eventG_input\
    ((sim_general_conf,
     sim_scenario_conf, 
     city_obj))

sim_eventG = run_eventG_sim\
    (simInput = simInput_eventG)

simOutput_eventG = EFFCS_SimOutput(sim_eventG)
#print (simOutput_eventG.sim_stats)
sim_stats = simOutput_eventG.sim_stats

#fig, ax = plt.subplots(1,1)
#grid.plot(color="white", edgecolor="black", ax=ax)
#grid.loc[simInput_eventG.valid_zones, "valid"] = True
#grid.dropna(subset=["valid"]).plot\
#    (color="lavender", edgecolor="blue", column="valid", ax=ax).plot()
#grid.iloc[200:201].plot(ax=ax)
#grid.iloc[350:351].plot(ax=ax)
#grid.iloc[620:621].plot(ax=ax)
