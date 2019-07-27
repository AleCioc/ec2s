import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

def plot_events_percentage (sim_stats_df, x_col, marker="o", label_add=""):

    label_add = " " + label_add
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.n_bookings / sim_stats_df.n_booking_reqs, 
         label = "satisfied" + label_add,
         marker=marker)
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.n_same_zone_trips / sim_stats_df.n_booking_reqs, 
         label = "same zone" + label_add,
         marker=marker)
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.n_not_same_zone_trips / sim_stats_df.n_booking_reqs, 
         label = "neighbor zone" + label_add,
         marker=marker)
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.n_deaths / sim_stats_df.n_booking_reqs, 
         label = "deaths" + label_add,
         marker=marker)
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.n_no_close_cars / sim_stats_df.n_booking_reqs, 
         label = "no available cars" + label_add,
         marker=marker)
    plt.xlabel(x_col)
    plt.ylabel("percentage of events")


def plot_param_cross_section (results_df, x_col, y_col, param_col):
    plt.figure(figsize=(15,7))
    plt.title(y_col)
    plt.ylabel(y_col)
    plt.xlabel(x_col)
    for param_value in results_df[param_col].unique():
        group_df = results_df.loc\
            [(results_df[param_col] == param_value)]
        plt.plot(group_df.hub_n_charging_poles, 
                 group_df.n_deaths / group_df.n_booking_reqs, 
                 marker="o", 
                 label=param_col + "=" + str(param_value))
    plt.legend()