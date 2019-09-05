import os

import pandas as pd

from DataStructures.City import City

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import run_eventG_sim

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

def single_run(city, sim_type, sim_general_conf, sim_scenario_conf):

    results_path = os.path.join(os.getcwd(), "Results", city, sim_type)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    sim_general_conf["city"] = city
    sim_general_conf["bin_side_length"] = 500

    city_obj = City\
        (city,
         sim_general_conf)

    simInput_eventG = get_eventG_input\
        ((sim_general_conf,
         sim_scenario_conf,
         city_obj))
    sim_eventG = run_eventG_sim\
        (simInput = simInput_eventG)
    simOutput_eventG = EFFCS_SimOutput(sim_eventG)
    sim_stats  = simOutput_eventG.sim_stats

    sim_stats.to_pickle\
        (os.path.join(results_path,
                      sim_type + ".pickle"))

    pd.Series(sim_general_conf).to_pickle\
        (os.path.join(results_path,
                      "sim_general_conf.pickle"))

    pd.Series(sim_scenario_conf).to_pickle\
        (os.path.join(results_path,
                      "sim_scenario_conf.pickle"))
