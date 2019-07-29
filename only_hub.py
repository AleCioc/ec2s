import datetime
import os
import sys
from pathlib import Path
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import read_sim_input_data

from DataStructures.City import City

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import get_eventG_sim_stats

city = sys.argv[1]

if not Path(os.path.join(os.getcwd(), "Results")).exists():
    os.mkdir(Path(os.path.join(os.getcwd(), "Results")))
    os.mkdir(Path(os.path.join(os.getcwd(), "Results", city)))
    os.mkdir(Path(os.path.join(os.getcwd(), "Results", city, "only_hub")))    
elif not Path(os.path.join(os.getcwd(), "Results", city)).exists():
    os.mkdir(Path(os.path.join(os.getcwd(), "Results", city)))
    os.mkdir(Path(os.path.join(os.getcwd(), "Results", city, "only_hub")))    
elif not Path(os.path.join(os.getcwd(), "Results", city, "only_hub")).exists():
    os.mkdir(Path(os.path.join(os.getcwd(), "Results", city, "only_hub")))    

"""
Init general conf and data structure
"""

sim_general_conf = {

    "city": city,
    "bin_side_length": 500,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 11, 1)

}
    
"""
Only hub ideal
"""

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],
        
    "time_estimation": [False],
    "queuing": [True, False],
    "alpha": [25],
    "beta": [60, 80, 100],

    "hub": [True],
    "hub_zone_policy": ["num_parkings"],
    "hub_n_charging_poles": np.arange(20, 80, 5),

    "relocation": [True],
    "finite_workers": [False],
    
    "distributed_cps": [False],
    "cps_placement_policy": ["num_parkings"],
    "n_charging_poles": [20],
    "cps_zones_percentage": [0.1],
    
    "user_contribution": [False],
    "system_cps": [False],
    "willingness": [0.99],
    
}

n_cores = 20

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
sim_stats_df.to_pickle("Results/" + city + "/only_hub/costnocost.pickle")