import os
import sys
import datetime

import pandas as pd

from Loading.create_input_pickles import create_input_pickles
from ModelValidation.model_validation import run_model_validation
from SingleRun.single_run import single_run
from MultipleRun.multiple_runs import multiple_runs
from SimulationOutput.EFFCS_MultipleRunsPlotter import plot_multiple_runs

from utils.path_utils import create_output_folders

confs_dict = {}
from SimulationInput.confs.sim_general_conf import sim_general_conf
from SimulationInput.confs.only_hub_conf import sim_scenario_conf_grid
confs_dict["only_hub"] = sim_scenario_conf_grid
from SimulationInput.confs.only_cps_conf import sim_scenario_conf_grid
confs_dict["only_cps"] = sim_scenario_conf_grid
from SimulationInput.confs.hub_cps_conf import sim_scenario_conf_grid
confs_dict["hub_cps"] = sim_scenario_conf_grid
from SimulationInput.confs.multiple_runs_conf import sim_scenario_conf_grid
confs_dict["trial"] = sim_scenario_conf_grid

n_cores = 4
print(n_cores)

for sim_scenario_name in ["only_hub", "only_cps"]:

	for city_name in ["Torino"]:

		print (datetime.datetime.now(), city_name)
		create_output_folders(city_name, sim_scenario_name)

		# create_input_pickles(city_name, [9, 10], 500)
		# run_model_validation(city_name)

		# from SimulationInput.confs.single_run_conf import sim_scenario_conf
		# single_run(city_name,
		#            sim_general_conf,
		#            sim_scenario_conf,
		#            "eventG",
		#            sim_scenario_name)

		multiple_runs(
			city_name,
			"multiple_runs",
			sim_general_conf,
			confs_dict[sim_scenario_name],
			int(n_cores),
			sim_scenario_name=sim_scenario_name
		)

		# plot_multiple_runs (city_name, sim_scenario_name)

	print (datetime.datetime.now())
