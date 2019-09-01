import sys
city_name = sys.argv[1]

# from Loading.create_input_pickles import run_create_pickles
# run_create_pickles(city_name)

from ModelValidation.model_validation import run_model_validation
run_model_validation(city_name)

# from MultipleRun.multiple_runs import multiple_runs
# from SimulationInput.confs.multiple_runs_conf import sim_general_conf
# from SimulationInput.confs.multiple_runs_conf import sim_scenario_conf_grid
# multiple_runs(city_name, "trial", sim_general_conf, sim_scenario_conf_grid)
