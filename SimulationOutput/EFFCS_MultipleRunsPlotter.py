import os

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

from MultipleRun.plot_multiple_runs import plot_events_percentage
from MultipleRun.plot_multiple_runs import plot_param_cross_section

class EFFCS_MultipleRunsPlotter():

    def __init__(self, sim_stats_df, city, sim_scenario_name = "trial"):

        self.sim_stats_df = sim_stats_df
        self.city = city

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "multiple_runs")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)
        self.figures_path = os.path.join\
            (os.getcwd(), "Figures", self.city, "multiple_runs", sim_scenario_name)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

        sim_stats_df_path = os.path.join("Results", city, "multiple_runs", sim_scenario_name, "sim_stats.pickle")
        self.sim_stats_df = pd.read_pickle(sim_stats_df_path)
        self.sim_stats_df = self.sim_stats_df[self.sim_stats_df.time_estimation == True]

        x_col = "hub_n_charging_poles"

    def plot_only_hub_qvsnoq ():

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]

        results_df_noq = \
            results_df[(results_df.queuing == False)]

        results_df_q_best_n_cars = \
            results_df[(results_df.queuing == True) \
                    & (results_df.n_cars_factor == 0.9)]

        results_df_noq_best_n_cars = \
            results_df[(results_df.queuing == False) \
                    & (results_df.n_cars_factor == 0.9)]

        results_df_q_best_beta = \
            results_df[(results_df.queuing == True) \
                    & (results_df.beta == 100)]

        results_df_noq_best_beta = \
            results_df[(results_df.queuing == False) \
                    & (results_df.beta == 100)]

        results_df_q_best = \
            results_df[(results_df.queuing == True) \
                   & (results_df.beta == 60) \
                   & (results_df.n_cars_factor == 0.9)]

        results_df_noq_best = \
            results_df[(results_df.queuing == False) \
                 & (results_df.beta == 100) \
                 & (results_df.n_cars_factor == 0.9)]

        x_col = "hub_n_charging_poles"

        plot_events_percentage\
            (results_df_q_best,
             x_col,
             "o",
             title_add=", queuing")

