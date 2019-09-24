import os
import sys
import datetime

import pandas as pd

from Loading.create_input_pickles import create_input_pickles
from ModelValidation.model_validation import run_model_validation
from SingleRun.single_run import single_run
from MultipleRun.multiple_runs import multiple_runs
from MultipleRun.multiple_runs import plot_multiple_runs

confs_dict = {}
from SimulationInput.confs.only_hub_conf import sim_general_conf
from SimulationInput.confs.only_hub_conf import sim_scenario_conf_grid
confs_dict["only_hub"] = sim_scenario_conf_grid
from SimulationInput.confs.only_cps_conf import sim_scenario_conf_grid
confs_dict["only_cps"] = sim_scenario_conf_grid
from SimulationInput.confs.hub_cps_conf import sim_scenario_conf_grid
confs_dict["hub_cps"] = sim_scenario_conf_grid
from SimulationInput.confs.multiple_runs_conf import sim_scenario_conf_grid
confs_dict["trial"] = sim_scenario_conf_grid

print (sys.argv[2:])
n_cores = sys.argv[1]
print(n_cores)
sim_scenario_name = sys.argv[2]

for city_name in sys.argv[3:]:

    print (datetime.datetime.now(), city_name)

    results_path = os.path.join\
        (os.getcwd(), "Results")
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join\
        (os.getcwd(), "Figures")
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join\
        (os.getcwd(), "Results", city_name)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join\
        (os.getcwd(), "Figures", city_name)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    # create_input_pickles(city_name, [9, 10], 500)
    # run_model_validation(city_name)

    # from SimulationInput.confs.single_run_conf import sim_general_conf
    # from SimulationInput.confs.single_run_conf import sim_scenario_conf
    # single_run(city_name, sim_general_conf, sim_scenario_conf, "eventG", sim_scenario_name)

    multiple_runs(city_name,
                  "multiple_runs",
                  sim_general_conf,
                  confs_dict[sim_scenario_name],
                  int(n_cores),
                  sim_scenario_name=sim_scenario_name)

    # plot_multiple_runs (city_name, sim_scenario_name)

print (datetime.datetime.now())
