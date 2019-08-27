import os
import multiprocessing as mp

import numpy as np
import pandas as pd

from DataStructures.City import City

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationInput.confs.multiple_runs_conf import sim_general_conf
from SimulationInput.confs.multiple_runs_conf import sim_scenario_conf_grid

def multiple_runs(city):

    sim_general_conf["city"] = city
    sim_general_conf["bin_side_length"] = 500
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
