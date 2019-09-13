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

        idxmin = self.sim_stats_df.percentage_unsatisfied.sort_values().index[0]

        self.city = city

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "multiple_runs")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)
        self.figures_path = os.path.join\
            (os.getcwd(), "Figures", self.city, "multiple_runs", sim_scenario_name)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

    def plot_events_profiles_qnoq_best \
        (self,
         x_col):

        results_df = self.sim_stats_df

        results_df_q_best = \
            results_df[(results_df.queuing == True) \
                   & (results_df.beta == 60) \
                   & (results_df.n_cars_factor == 0.9)]

        results_df_noq_best = \
            results_df[(results_df.queuing == False) \
                 & (results_df.beta == 100) \
                 & (results_df.n_cars_factor == 0.9)]

        plot_events_percentage\
            (results_df_q_best,
             x_col=x_col,
             title_add=", queuing",
             figpath=self.figures_path,
             figname="events_profile_queuing_best")

        plot_events_percentage\
            (results_df_noq_best,\
             x_col=x_col,\
             title_add=", no queuing",
             figpath=self.figures_path,
             figname="events_profile_noqueuing_best")

    def plot_cross_sections_beta_n_cars_qnoq (
            self, 
            x_col="hub_n_charging_poles", 
            param_col="beta",
            n_cars_factor=0.9,
            beta=60):

        results_df = self.sim_stats_df

        results_df_q_best_n_cars = \
            results_df[(results_df.queuing == True) \
                    & (results_df.n_cars_factor == n_cars_factor)]

        results_df_q_best_beta = \
            results_df[(results_df.queuing == True) \
                    & (results_df.beta == beta)]

        x_col = x_col
        param_col = param_col

        for y_col in ["percentage_unsatisfied",
                      "cum_relo_t"]:

            if param_col == "n_cars_factor":

                plot_param_cross_section \
                    (results_df_q_best_beta,
                     x_col, 
                     y_col, 
                     param_col,
                     "beta = " + str(beta),
                     figpath=self.figures_path,
                     figname="_".join([y_col, param_col]))

            elif param_col == "beta":

                plot_param_cross_section \
                    (results_df_q_best_n_cars,
                     x_col, 
                     y_col, 
                     param_col,
                     "n_cars_factor = " + str(n_cars_factor),
                     figpath=self.figures_path,
                     figname="_".join([y_col, param_col]))

    def plot_3d (self, df_plot, x_col, y_col, z_col, fixed_param_col, fixed_param_value,
                 title_add=""):

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
        plt.title(z_col + " = f (" + x_col + ", " + y_col + ")" + title_add)

        plt.savefig(os.path.join(self.figures_path, "_".join\
            ([z_col, x_col, y_col, fixed_param_col, str(fixed_param_value), ".png"])))

    def plot_beta_n_cars_3d (self, 
                            z_col='percentage_unsatisfied',
                            x_col="n_cars_factor",
                            y_col="beta",
                            hub_n_charging_poles=50
                            ):

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]
        df_plot = results_df_q[results_df_q.hub_n_charging_poles == hub_n_charging_poles]
        self.plot_3d(df_plot, x_col, y_col, z_col, "hub_n_charging_poles", hub_n_charging_poles,
                     title_add=", hub_n_charging_poles = " + str(hub_n_charging_poles))

    def plot_beta_n_poles_3d (self,
                            z_col='percentage_unsatisfied',
                            x_col="beta",
                            y_col="hub_n_charging_poles",
                            n_cars_factor=0.9
                            ):

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]
        df_plot = results_df_q[results_df_q.n_cars_factor == n_cars_factor]
        self.plot_3d(df_plot, x_col, y_col, z_col, "n_cars_factor", n_cars_factor,
                     title_add=", n_cars_factor = " + str(n_cars_factor))

    def plot_n_poles_n_cars_3d (self,
                            z_col='percentage_unsatisfied',
                            x_col="n_cars_factor",
                            y_col="hub_n_charging_poles",
                            beta=60
                            ):

        results_df = self.sim_stats_df

        results_df_q = \
            results_df[(results_df.queuing == True)]
        df_plot = results_df_q[results_df_q.beta == beta]
        self.plot_3d(df_plot, x_col, y_col, z_col, "beta", beta,
                     title_add=", beta = " + str(beta))
