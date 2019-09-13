import os
import sys
import datetime

from Loading.create_input_pickles import create_input_pickles
from ModelValidation.model_validation import run_model_validation
from SingleRun.single_run import single_run
from MultipleRun.multiple_runs import multiple_runs

print (sys.argv[2:])

for city_name in sys.argv[2:]:

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
    # single_run(city_name, sim_general_conf, sim_scenario_conf, "eventG", "only_hub_eventG_ideal")

    # from SimulationInput.confs.multiple_runs_conf import sim_general_conf
    # from SimulationInput.confs.only_hub_conf import sim_scenario_conf_grid
    # n_cores = sys.argv[1]
    # print (n_cores)
    # multiple_runs(city_name,
    #               "only_hub",
    #               sim_general_conf,
    #               sim_scenario_conf_grid,
    #               int(n_cores),
    #               sim_scenario_name="only_hub")

    import pandas as pd
    results_path = os.path.join \
        (os.getcwd(), "Results", city_name, "multiple_runs", "only_hub", "sim_stats.pickle")
    sim_stats_df = pd.read_pickle(results_path)

    from SimulationOutput.EFFCS_MultipleRunsPlotter import EFFCS_MultipleRunsPlotter

    plotter = EFFCS_MultipleRunsPlotter(sim_stats_df,
                                        city_name,
                                        "only_hub")

    x_col = "hub_n_charging_poles"

    plotter.plot_events_profiles_qnoq_best\
        (x_col=x_col)

    plotter.plot_cross_sections_beta_n_cars_qnoq\
        (x_col=x_col, 
         param_col="beta")

    plotter.plot_cross_sections_beta_n_cars_qnoq\
        (x_col=x_col, 
         param_col="n_cars_factor")

    plotter.plot_beta_n_cars_3d\
        (z_col="percentage_unsatisfied")

    plotter.plot_n_poles_n_cars_3d\
        (z_col="percentage_unsatisfied",
         y_col=x_col)

    plotter.plot_beta_n_cars_3d\
        (z_col="percentage_deaths")

    plotter.plot_n_poles_n_cars_3d\
        (z_col="percentage_deaths",
         y_col=x_col)

    plotter.plot_beta_n_cars_3d(z_col="cum_relo_t")

    plotter.plot_n_poles_n_cars_3d(z_col="cum_relo_t")

print (datetime.datetime.now())