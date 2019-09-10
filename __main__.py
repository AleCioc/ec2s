import sys

from Loading.create_input_pickles import create_input_pickles
from ModelValidation.model_validation import run_model_validation
from SingleRun.single_run import single_run
from MultipleRun.multiple_runs import multiple_runs

print (sys.argv[2:])

for city_name in sys.argv[2:]:

    # create_input_pickles(city_name, [9, 10], 500)
    # run_model_validation(city_name)

    # from SimulationInput.confs.single_run_conf import sim_general_conf
    # from SimulationInput.confs.single_run_conf import sim_scenario_conf
    # single_run(city_name, "single_run", sim_general_conf, sim_scenario_conf)

    from SimulationInput.confs.multiple_runs_conf import sim_general_conf
    from SimulationInput.confs.only_hub_conf import sim_scenario_conf_grid
    n_cores = sys.argv[1]
    multiple_runs(city_name, "only_hub", sim_general_conf, sim_scenario_conf_grid, int(n_cores))
