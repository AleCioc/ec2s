import os
import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from DataStructures.City import City

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_MultipleRunsPlotter import EFFCS_MultipleRunsPlotter

def plot_multiple_runs (city_name,
                        sim_scenario_name):

    results_path = os.path.join\
        (os.getcwd(), "Figures", city_name, "multiple_runs")
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join\
        (os.getcwd(), "Figures", city_name, "multiple_runs", sim_scenario_name)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join \
        (os.getcwd(), "Results", city_name, "multiple_runs", sim_scenario_name, "sim_stats.pickle")
    sim_stats_df = pd.read_pickle(results_path)
    for col in sim_stats_df:
        if col.startswith("percentage"):
            sim_stats_df[col] = \
                sim_stats_df[col] * 100

    plotter = EFFCS_MultipleRunsPlotter(sim_stats_df,
                                        city_name,
                                        sim_scenario_name)
    print(plotter.best_params_unsatisfied)
    print(plotter.best_params_relocost)

    x_col = "n_poles_n_cars_factor"
    y_col = "n_cars_factor"
    fixed_param_col = "beta"

    for z_col in ["percentage_unsatisfied",
                  "cum_relo_t"]:

        # for fixed_param_value in sim_stats_df[fixed_param_col].unique():
        #     plotter.plot_3d\
        #         (x_col=x_col,
        #          y_col=y_col,
        #          z_col=z_col,
        #          fixed_param_col=fixed_param_col,
        #          fixed_param_value=fixed_param_value,
        #          title_add=fixed_param_col + "=" + str(fixed_param_value))

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="beta",
             fixed_params_dict=
                {"n_cars_factor":plotter.best_params_unsatisfied.loc["n_cars_factor"],
                 "willingness":plotter.best_params_unsatisfied.loc["willingness"]},
             figname="best_unsatisfied")

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="n_cars_factor",
             fixed_params_dict=
                {"beta":plotter.best_params_unsatisfied.loc["beta"],
                 "willingness":plotter.best_params_unsatisfied.loc["willingness"]},
             figname="best_unsatisfied")

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="willingness",
             fixed_params_dict=
                {"n_cars_factor":plotter.best_params_unsatisfied.loc["n_cars_factor"],
                 "beta":plotter.best_params_unsatisfied.loc["beta"]},
             figname="best_unsatisfied")

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="beta",
             fixed_params_dict=
                {"n_cars_factor":plotter.best_params_relocost.loc["n_cars_factor"],
                 "willingness":plotter.best_params_relocost.loc["willingness"]},
             figname="best_relocost")

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="n_cars_factor",
             fixed_params_dict=
                {"beta":plotter.best_params_relocost.loc["beta"],
                 "willingness":plotter.best_params_relocost.loc["willingness"]},
             figname="best_relocost")

        plotter.plot_cross_sections\
            (y_col=z_col,
             x_col=x_col,
             param_col="willingness",
             fixed_params_dict=
                {"n_cars_factor":plotter.best_params_relocost.loc["n_cars_factor"],
                 "beta":plotter.best_params_relocost.loc["beta"]},
             figname="best_relocost")

    plotter.plot_events_profiles\
        (x_col=x_col,
         params_dict=
                {"beta":plotter.best_params_unsatisfied.loc["beta"],
                 "n_cars_factor": plotter.best_params_unsatisfied.loc["n_cars_factor"],
                 "willingness":plotter.best_params_unsatisfied.loc["willingness"]},
         figname_add="_min_unsatisfied")

    plotter.plot_events_profiles\
        (x_col=x_col,
         params_dict=
                {"beta":plotter.best_params_relocost.loc["beta"],
                 "n_cars_factor": plotter.best_params_relocost.loc["n_cars_factor"],
                 "willingness":plotter.best_params_relocost.loc["willingness"]},
         figname_add="_min_relocost")

def multiple_runs(city, sim_type, sim_general_conf, sim_scenario_conf_grid,
                  n_cores = 4, sim_scenario_name="trial"):

    results_path = os.path.join\
        (os.getcwd(), "Results", city, "multiple_runs")
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    results_path = os.path.join \
        (os.getcwd(), "Results", city, "multiple_runs", sim_scenario_name)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    sim_general_conf["city"] = city
    sim_general_conf["bin_side_length"] = 500

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

            print ("Batch", i / n_cores, datetime.datetime.now())

    sim_stats_df = pd.concat\
        ([sim_stats for sim_stats in pool_stats_list],
         axis=1, ignore_index=True).T

    sim_stats_df.to_pickle\
        (os.path.join(results_path,
                      "sim_stats.pickle"))

    pd.Series(sim_general_conf).to_pickle\
        (os.path.join(results_path,
                      "sim_general_conf.pickle"))

    pd.Series(sim_scenario_conf_grid).to_pickle\
        (os.path.join(results_path,
                      "sim_scenario_conf_grid.pickle"))
