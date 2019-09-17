import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

def plot_events_percentage (sim_stats_df, 
                            x_col, 
                            title_add,
                            figpath,
                            figname):

    plt.figure(figsize=(15, 7))
    plt.title("Percentage of satisfied events" + title_add)
    plt.ylim(0, 1)
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_same_zone_trips_satisfied, 
         label = "same zone",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_not_same_zone_trips_satisfied, 
         label = "neighbor zone",
         marker="o")

    plt.xlabel(x_col)
    plt.ylabel("percentage of satisfied events")
    plt.legend()
    plt.savefig(os.path.join(figpath, figname + "_satisfied", ".pdf"))
    plt.close()

    plt.figure(figsize=(15, 7))
    plt.title("Percentage of unsatisfied events" + title_add)
    plt.ylim(0, 1)

    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_deaths_unsatisfied, 
         label = "not enough energy",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_no_close_cars_unsatisfied, 
         label = "no available cars",
         marker="o")

    plt.xlabel(x_col)
    plt.ylabel("percentage of unsatisfied events")
    plt.legend()
    plt.savefig(os.path.join(figpath, figname + "_unsatisfied", ".pdf"))
    plt.close()

def plot_param_cross_section (results_df, 
                              x_col, 
                              y_col, 
                              param_col,
                              figpath,
                              figname,
                              fixed_params_dict):

    plt.figure(figsize=(15, 7))
    plt.title(y_col + ", varying " + param_col + ", " + str(fixed_params_dict))
    plt.ylabel(y_col)
    plt.xlabel(x_col)
    for param_value in results_df[param_col].unique():
        group_df = results_df.loc\
            [(results_df[param_col] == param_value)]
        plt.plot(group_df[x_col], 
                 group_df[y_col], 
                 marker="o", 
                 label=param_col + "=" + str(param_value))
    
    plt.legend()
    plt.savefig(os.path.join(figpath, figname, ".pdf"))
#    plt.show()
    plt.close()

