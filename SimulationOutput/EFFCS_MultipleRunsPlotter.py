import os

import numpy as np

from SimulationOutput.plot_multiple_runs import plot_events_percentage
from SimulationOutput.plot_multiple_runs import plot_param_cross_section

class EFFCS_MultipleRunsPlotter():

    def __init__(self, sim_stats_df, city, sim_scenario_name = "trial"):

        self.sim_stats_df = sim_stats_df.copy()

        self.sim_stats_df = self.sim_stats_df[self.sim_stats_df.time_estimation == True]
        self.sim_stats_df.n_cars_factor = \
            self.sim_stats_df.n_cars_factor.apply(lambda x: np.around(x, decimals=2))

        self.sim_stats_df["percentage_unsatisfied"] = \
            100 - self.sim_stats_df.percentage_satisfied

        if sim_scenario_name == "hub_cps":
            self.sim_stats_df = self.sim_stats_df\
                [self.sim_stats_df.willingness > 0.1]

        # print (self.sim_stats_df.n_booking_reqs)
        # print (self.sim_stats_df.n_bookings)
        # print (self.sim_stats_df.n_unsatisfied)
        # print (self.sim_stats_df.percentage_unsatisfied)
        # print (self.sim_stats_df.percentage_satisfied)
        # print (self.sim_stats_df.alpha.unique())

        self.idxmin_unsatisfied = self.sim_stats_df.percentage_unsatisfied.sort_values().index[0]
        self.idxmin_relocost = self.sim_stats_df.cum_relo_t.sort_values().index[0]
        print (self.sim_stats_df.loc[self.idxmin_unsatisfied, "percentage_unsatisfied"],
               self.sim_stats_df.loc[self.idxmin_relocost, "cum_relo_t"])
        print(self.idxmin_unsatisfied, self.idxmin_relocost)
        self.best_params_unsatisfied = (self.sim_stats_df.loc[self.idxmin_unsatisfied,
                                     ["beta", "willingness", "n_cars_factor"]])
        self.best_params_relocost = (self.sim_stats_df.loc[self.idxmin_relocost,
                                     ["beta", "willingness", "n_cars_factor"]])
        self.city = city

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "multiple_runs")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)
        self.figures_path = os.path.join\
            (os.getcwd(), "Figures", self.city, "multiple_runs", sim_scenario_name)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

    def plot_cross_sections (
            self,
            y_col,
            x_col,
            param_col,
            fixed_params_dict,
		    figname):

        results_df = self.sim_stats_df

        results_df_q = results_df[results_df.queuing == True]

        for fixed_param_col in fixed_params_dict:
            results_df_q = results_df_q\
                [results_df_q[fixed_param_col] == fixed_params_dict[fixed_param_col]]

        plot_param_cross_section \
            (results_df_q,
             x_col,
             y_col,
             param_col,
             figpath=self.figures_path,
             figname="_".join\
                 ([y_col, param_col, figname]),
             fixed_params_dict=fixed_params_dict)

    def plot_events_profiles \
        (self,
         x_col,
         params_dict,
         figname_add=""):

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]

        for param_col in params_dict:
            results_df_q = \
                results_df_q[results_df_q[param_col] == params_dict[param_col]]

        plot_events_percentage\
            (results_df_q,
             x_col=x_col,
             title_add=str(params_dict),
             figpath=self.figures_path,
             figname="events_profile" + figname_add)
