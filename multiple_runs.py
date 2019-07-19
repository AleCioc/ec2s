import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from SimulationInput.EFFCS_SimConfGrid import EFFCS_SimConfGrid

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_traceB_sim import run_traceB_sim
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Read input data and create input pickles
"""

#bookings,\
#parkings,\
#grid,\
#bookings_origins_gdf,\
#bookings_destinations_gdf,\
#parkings_gdf = get_input_data\
#    ("Torino", [9, 10], 500)

#bookings, grid = read_sim_input_data("Torino")

"""
Init general conf and data structure
"""

sim_general_conf = {

    "city": "Torino",
    "bin_side_length": 500,
    "requests_rate_factor": 1,
    "model_start" : datetime.datetime(2017, 9, 1),
    "model_end" : datetime.datetime(2017, 10, 1),
    "sim_start" : datetime.datetime(2017, 10, 1),
    "sim_end" : datetime.datetime(2017, 11, 1)

}
    
sim_scenario_conf_grid = {

    "n_cars": [350],

    "time_estimation": [False],
    "queuing": [True, False],
    "alpha": [25],
    "beta": [100],

    "hub": [True],
    "hub_zone_policy": ["default"],
    "hub_zone": [2501],
    "hub_n_charging_poles": np.arange(20, 105, 5),
    "relocation": [False],
    "finite_workers": [False],
    
    "distributed_cps": [False],
    "cps_placement_policy": ["default"],
    "n_charging_poles": [200],
    "cps_zones_percentage": [0.1],
    
    "user_contribution": [False],
    "willingness": [0.99],    
    
}


"""
Multiple Runs with multiprocessing
"""

with mp.Pool(2) as pool:

    bookings, grid = read_sim_input_data\
        (sim_general_conf["city"])
                        
    sim_conf_grid = EFFCS_SimConfGrid\
        (sim_general_conf, sim_scenario_conf_grid)

    sim_inputs = []
    for sim_scenario_conf in sim_conf_grid.conf_list:
        simInput_eventG = get_eventG_input\
            (sim_general_conf,
             sim_scenario_conf, 
             grid,
             bookings)
        sim_inputs += [simInput_eventG]

    pool_stats_df = pool.map\
        (get_eventG_sim_stats, sim_inputs)

sim_stats_df = pd.concat\
    ([s for s in pool_stats_df], axis=1, ignore_index=True).T

x_col = "hub_n_charging_poles"
vs_col = "queuing"
sim_stats_df.to_pickle("Results/Torino/only_hub/" + x_col + "_" + vs_col + ".pickle")

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

def plot_results ():


	plt.figure(figsize=(15, 7))
	plt.title("Percentage of events, Torino, one month")
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.n_bookings / sim_stats_df.n_booking_reqs, 
		     label = "satisfied",
		     marker="o")
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.n_deaths / sim_stats_df.n_booking_reqs, 
		     label = "deaths",
		     marker="o")
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.n_no_close_cars / sim_stats_df.n_booking_reqs, 
		     label = "no available cars",
		     marker="o")
	plt.xlabel([x_col])
	plt.ylabel("percentage of events")
	plt.legend()
	plt.savefig("Figures/Torino/only_hub/" + x_col + "_events_" + vs_col + ".png")
	#plt.show()
	plt.close()

	plt.title("Percentage of events, Torino, one month")
	plt.figure(figsize=(15, 7))
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.tot_energy, 
		     label = "charging energy",
		     marker="o")
	plt.xlabel("n_cars")
	plt.ylabel("charging energy [kwh]")
	plt.legend()
	plt.savefig("Figures/Torino/only_hub/" + x_col + "_tot-energy_" + vs_col + ".png")
	#plt.show()
	plt.close()

	plt.figure(figsize=(15, 7))
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.percentage_charges_system, 
		     label = "system charges",
		     marker="o")
	plt.plot(sim_stats_df[x_col], 
		     sim_stats_df.percentage_charges_users, 
		     label = "user charges",
		     marker="o")
	plt.xlabel("n_cars")
	plt.ylabel("percentage of charges")
	plt.legend()
	plt.savefig("Figures/Torino/only_hub/" + x_col + "_charges_" + vs_col + ".png")
	#plt.show()
	plt.close()

#plot_results()

