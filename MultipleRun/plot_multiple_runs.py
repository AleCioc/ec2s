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
    plt.title("Percentage of events" + title_add)    

    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_satisfied, 
         label = "satisfied",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_same_zone_trips, 
         label = "same zone",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_not_same_zone_trips, 
         label = "neighbor zone",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_deaths, 
         label = "deaths",
         marker="o")
    
    plt.plot(sim_stats_df[x_col], 
         sim_stats_df.percentage_no_close_cars, 
         label = "no available cars",
         marker="o")
    
    plt.xlabel(x_col)
    plt.ylabel("percentage of events")
    plt.legend()
    plt.savefig(os.path.join(figpath,figname))
#    plt.show()
    plt.close()

def plot_param_cross_section (results_df, 
                              x_col, 
                              y_col, 
                              param_col,
                              title_add,
                              figpath,
                              figname):

    plt.figure(figsize=(15, 7))
    plt.title(y_col + ", " + title_add)
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
    plt.savefig(os.path.join(figpath, figname))
#    plt.show()
    plt.close()

