import os
import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from DataStructures.City import City

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.run_traceB_sim import run_traceB_sim

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_output
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput


"""
Init general conf and data structure
"""

sim_general_conf = {

    "city": "Torino",
    "bin_side_length": 500,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 11, 1)

}
    
sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],

    "time_estimation": [True],
    "queuing": [True],
    "alpha": [25],
    "beta": [40, 60, 80, 90],

    "hub": [False],
    "hub_zone_policy": ["default"],
    "hub_zone": [350],
    "hub_n_charging_poles": [10, 20, 30, 40],

    "relocation": [True],
    "finite_workers": [False],
    
    "distributed_cps": [True],
    "cps_placement_policy": ["default"],
    "n_charging_poles": [20],
    "cps_zones_percentage": [0.1],
    
    "user_contribution": [True],
    "system_cps": [True],
    "willingness": [0.99],
    
}

"""
Multiple Runs with multiprocessing
"""

n_cores = 4
with mp.Pool(n_cores) as pool:

    city_obj = City\
        (sim_general_conf["city"],
         sim_general_conf)                        

    sim_conf_grid = EFFCS_SimConfGrid\
        (sim_general_conf, sim_scenario_conf_grid)

    pool_stats_list = []
    for i in np.arange(0, len(sim_conf_grid.conf_list), n_cores):

        conf_tuples = []
        for sim_scenario_conf in sim_conf_grid.conf_list[i: i + n_cores]:
            conf_tuples += [(sim_general_conf,
                            sim_scenario_conf,
                            city_obj)]

        sim_inputs = pool.map\
            (get_eventG_input, conf_tuples)

        pool_stats_list += pool.map\
            (get_eventG_sim_stats, sim_inputs)

sim_stats_df = pd.concat\
    ([sim_stats for sim_stats in pool_stats_list], 
     axis=1, ignore_index=True).T

sim_stats_df.to_pickle\
    (os.path.join(os.getcwd(), 
                  "Results",
                  "trial.pickle"))
