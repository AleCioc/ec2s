import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_traceB_sim import run_traceB_sim
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Read input data and create input pickles
"""

#bookings,\
#parkings,\
#grid,\
#bookings_origins_gdf,\
#bookings_destinations_gdf,\
#parkings_gdf = get_input_data\
#    ("Torino", [9, 10], 500)

bookings, grid = read_sim_input_data("Torino")

"""
Init general conf and data structure
"""

sim_general_conf = {

    "city": "Torino",
    "bin_side_length": 500,
    "requests_rate_factor": 1,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 11, 1)

}
    
sim_scenario_conf = {

    "n_cars": 400,

    "time_estimation": False,
    "queuing": True,
    "alpha": 25,
    "beta": 100,

    "hub": True,
    "hub_zone_policy": "default",
    "hub_zone": 2501,
    "hub_n_charging_poles": 50,
    "relocation": False,
    "finite_workers": False,
    
    "distributed_cps": False,
    "cps_placement_policy": "default",
    "n_charging_poles": 200,
    "cps_zones_percentage": 0.1,
    
    "user_contribution": False,
    "willingness": 0.99,    
    
}

"""
Single Run
"""

simInput_eventG = get_eventG_input\
    (sim_general_conf,
     sim_scenario_conf, 
     grid,
     bookings)

sim_eventG = run_eventG_sim\
    (simInput = simInput_eventG)

simOutput_eventG = EFFCS_SimOutput(sim_eventG)
#print (simOutput_eventG.sim_stats)
