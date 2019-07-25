import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

path = "/".join(["Results", "Torino", "only_hub/"])
path += "poles-beta-cost.pickle"
x_col = "hub_n_charging_poles"

results_df = pd.read_pickle(path)
sim_stats_df = results_df[(results_df.queuing == True)\
                          & (results_df.beta == 100)]

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
plt.savefig("Figures/Torino/only_hub/" + x_col + "_events.png")
plt.show()
plt.close()

plt.figure(figsize=(15, 7))
plt.title("Tot charging energy, Torino, one month")
plt.plot(sim_stats_df[x_col], 
	     sim_stats_df.tot_energy, 
	     label = "charging energy",
	     marker="o")
plt.xlabel("n_cars")
plt.ylabel("charging energy [kwh]")
plt.legend()
plt.savefig("Figures/Torino/only_hub/" + x_col + "_tot-energy.png")
plt.show()
plt.close()

plt.figure(figsize=(15, 7))
plt.title("System vs user charges, Torino, one month")
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
plt.savefig("Figures/Torino/only_hub/" + x_col + "_charges.png")
plt.show()
plt.close()
