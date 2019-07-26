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


