import os

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

from MultipleRun.plot_multiple_runs import plot_events_percentage
from MultipleRun.plot_multiple_runs import plot_param_cross_section

class EFFCS_MultipleRunsPlotter():

    def __init__(self, sim_stats_df, city, sim_scenario_name = "trial"):

        self.sim_stats_df = sim_stats_df.copy()

        self.sim_stats_df["percentage_unsatisfied"] = \
            1.0 - self.sim_stats_df["percentage_satisfied"]
        self.sim_stats_df = self.sim_stats_df[self.sim_stats_df.time_estimation == True]
        self.sim_stats_df.n_cars_factor = \
            self.sim_stats_df.n_cars_factor.apply(lambda x: np.around(x, decimals=2))
        if sim_scenario_name == "hub_cps":
            self.sim_stats_df = self.sim_stats_df\
                [self.sim_stats_df.willingness > 0.1]

        self.idxmin_unsatisfied = self.sim_stats_df.percentage_unsatisfied.sort_values().index[0]
        self.idxmin_relocost = self.sim_stats_df.cum_relo_t.sort_values().index[0]
        print (self.sim_stats_df.loc[self.idxmin_unsatisfied, "percentage_unsatisfied"],
               self.sim_stats_df.loc[self.idxmin_relocost, "cum_relo_t"])
        print(self.idxmin_unsatisfied, self.idxmin_relocost)
        print (self.sim_stats_df.loc[self.idxmin_unsatisfied,
                                     ["beta", "willingness", "n_cars_factor"]])
        print (self.sim_stats_df.loc[self.idxmin_relocost,
                                     ["beta", "willingness", "n_cars_factor"]])
        self.city = city

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "multiple_runs")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)
        self.figures_path = os.path.join\
            (os.getcwd(), "Figures", self.city, "multiple_runs", sim_scenario_name)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

    def plot_3d (self,
                 x_col,
                 y_col,
                 z_col,
                 fixed_param_col,
                 fixed_param_value,
                 title_add=""):

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]

        df_plot = results_df_q\
            [results_df_q[fixed_param_col] == fixed_param_value]

        table = pd.pivot(df_plot,
                       values=z_col,
                       index=x_col,
                       columns=y_col)

        x, y = np.meshgrid(table.index, table.columns)
        z = table.T.values
        ax = plt.axes(projection="3d")
        ax.plot_wireframe(x, y, z, color='green')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
        plt.title(z_col + " = f (" + x_col + ", " + y_col + "), " + title_add)

        plt.savefig(os.path.join(self.figures_path, "_".join\
            ([z_col, x_col, y_col, fixed_param_col, str(fixed_param_value), "3d.png"])))

    def plot_cross_sections (
            self,
            y_col,
            x_col,
            param_col,
            fixed_params_dict):

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
                 ([y_col, param_col] +
                  ["_".join([t[0], str(t[1]).replace(".","-")])
                   for t in fixed_params_dict.items()]),
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
