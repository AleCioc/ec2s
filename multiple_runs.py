import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.run_traceB_sim import run_traceB_sim

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_output
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Create input pickles
"""

#bookings,\
#parkings,\
#grid,\
#bookings_origins_gdf,\
#bookings_destinations_gdf,\
#parkings_gdf = get_input_data\
#    ("Torino", [9, 10], 500)

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
    
sim_scenario_conf_grid = {

    "n_cars": [350],

    "time_estimation": [True],
    "queuing": [True],
    "alpha": [25],
    "beta": [60, 80, 100],

    "hub": [False],
    "hub_zone_policy": ["default"],
    "hub_zone": [350],
    "hub_n_charging_poles": [10],

    "relocation": [True, False],
    "finite_workers": [False],
    
    "distributed_cps": [True],
    "cps_placement_policy": ["default"],
    "n_charging_poles": np.arange(20, 81, 5),
    "cps_zones_percentage": [0.1],
    
    "user_contribution": [True],
    "system_cps": [True],
    "willingness": [0.99],
    
}

"""
Multiple Runs with multiprocessing
"""

with mp.Pool(4) as pool:

    bookings, grid = read_sim_input_data\
        (sim_general_conf["city"])
                        
    sim_conf_grid = EFFCS_SimConfGrid\
        (sim_general_conf, sim_scenario_conf_grid)

    pool_stats_list = []
    for i in np.arange(0, len(sim_conf_grid.conf_list), 4):

        conf_tuples = []
        for sim_scenario_conf in sim_conf_grid.conf_list[i: i+4]:
            conf_tuples += [(sim_general_conf,
                            sim_scenario_conf,
                            grid,
                            bookings)]

        sim_inputs = pool.map\
            (get_eventG_input, conf_tuples)

        pool_stats_list += pool.map\
            (get_eventG_sim_stats, sim_inputs)

sim_stats_df = pd.concat\
    ([sim_stats for sim_stats in pool_stats_list], 
     axis=1, ignore_index=True).T

sim_stats_df.to_pickle("Results/Torino/only_cps/poles-beta-cost-users.pickle")


