import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

#from pandas.plotting import scatter_matrix
#scatter_matrix(
#        sim_bookings[[
#                    "duration",
#                    "euclidean_distance",
#                    "start_soc",
#                    "end_soc"
#                ]]
#        )

def EFFCS_SimOutputPlotter ():
    
    def __init__ (simOutput):
        
        pass

sim_booking_requests = \
    simOutput_eventG.sim_booking_requests   

sim_bookings = \
    simOutput_eventG.sim_booking_requests   

sim_charges = \
    simOutput_eventG.sim_charges

sim_deaths = \
    simOutput_eventG.sim_deaths

sim_unsatisfied_requests = \
    simOutput_eventG.sim_unsatisfied_requests

sim_system_charges_bookings = \
    simOutput_eventG.sim_system_charges_bookings

sim_users_charges_bookings = \
    simOutput_eventG.sim_users_charges_bookings
sim_cars_events = pd.concat\
    ([sim_bookings, sim_charges], ignore_index=True, sort=False)\
    .sort_values("start_time")

#plt.figure()
#sim_charges.duration.apply\
#    (lambda x: x/60).hist\
#    (bins=50, cumulative=False, density=True)
#plt.title("charge duration histogram")
#plt.xlabel("hours")
#plt.show()
#plt.close()
#
#plt.figure()
#(sim_charges.sort_values\
#    ("start_time").groupby\
#    ("hour").date.count() / len(sim_charges.date.unique()))\
#    .plot(marker="o")
#plt.title("average number of charging events by hour")
#plt.xlabel("hour")
#plt.ylabel("n charges")
#plt.show()
#plt.close()
#
#plt.figure()
#(sim_charges.sort_values\
#    ("start_time").groupby\
#    ("hour").soc_delta_kwh.sum() / len(sim_charges.date.unique()))\
#    .plot(marker="o")
#plt.title("average charging energy by hour")
#plt.xlabel("hour")
#plt.ylabel("E [kwh]")
#plt.show()
#plt.close()
#
#plt.figure()
#sim_system_charges_bookings.set_index\
#    ("start_time").resample\
#    ("60Min").destination_id.count().plot(label="system")
#if len(sim_users_charges_bookings):
#    sim_users_charges_bookings.set_index\
#        ("start_time").resample\
#        ("60Min").destination_id.count().plot(label="users")
#plt.title("number of charging events sum by hour in time")
#plt.legend()
#plt.xlabel("t")
#plt.ylabel("n charges")
#plt.show()
#plt.close()
#
#plt.figure()
#sim_charges.sort_values\
#    ("start_time").groupby\
#    ("day_hour").soc_delta_kwh.sum().plot()
#plt.title("charging energy sum by hour in time")
#plt.xlabel("t")
#plt.ylabel("E [kwh]")
#plt.show()
#plt.close()
#
#plt.figure()
#sim_booking_requests\
#    .set_index("start_time")\
#    .n_cars_charging_system\
#    .plot(label="system charging", linewidth=2, alpha=0.7)
#sim_booking_requests\
#    .set_index("start_time")\
#    .n_cars_charging_users\
#    .plot(label="users charging", linewidth=2, alpha=0.7)
#sim_booking_requests\
#    .set_index("start_time")\
#    .n_cars_booked\
#    .plot(label="booked", linewidth=2, alpha=0.7)
#sim_booking_requests\
#    .set_index("start_time")\
#    .n_cars_available\
#    .plot(label="available", linewidth=2, alpha=0.7)
#plt.legend()
#plt.title("number of cars charging/available/booked in time")
#plt.xlabel("t")
#plt.ylabel("E [kwh]")
#plt.show()
#plt.close()
#
plt.figure()
sim_booking_requests\
    .set_index("start_time")\
    .n_cars_charging_system\
    .plot(label="system charging", linewidth=2, alpha=0.7)
sim_booking_requests\
    .set_index("start_time")\
    .n_cars_charging_users\
    .plot(label="users charging", linewidth=2, alpha=0.7)
plt.legend()
plt.title("number of cars charging in time")
plt.xlabel("t")
plt.ylabel("n cars")
plt.show()
plt.close()
#
#plt.figure()
#sim_system_charges_bookings["end_hour"].hist\
#    (bins=24, alpha=0.7, density=True,
#          label="system")
#sim_users_charges_bookings["end_hour"].hist\
#    (bins=24, alpha=0.7, density=True,
#          label="users")
#plt.legend()
#plt.title("charging timestamps histogram system vs users")
#plt.xlabel("hour")
#plt.show()
#plt.close()
#
#plt.figure()
#sim_system_charges_bookings["destination_id"]\
#    .hist(bins=20, alpha=0.7, density=False,
#          label="system")
#sim_users_charges_bookings["destination_id"]\
#    .hist(bins=20, alpha=0.7, density=False,
#          label="users")
#plt.legend()
#plt.title("charging needed locations histogram system vs users")
#plt.xlabel("zone id")
#plt.show()
#plt.close()

#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["origin_count"] = \
#    sim_booking_requests.origin_id.value_counts()
#grid.dropna(subset=["origin_count"])\
#    .plot(column="origin_count", ax=ax, legend=True)
#plt.title("origin heatmap")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()
#
#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["destination_count"] = \
#    sim_booking_requests.destination_id.value_counts()
#grid.dropna(subset=["destination_count"])\
#    .plot(column="destination_count", ax=ax, legend=True)
#plt.title("destination heatmap")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()

#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["charge_needed_system_zones_count"] = \
#    sim_system_charges_bookings.destination_id.value_counts()
#grid.dropna(subset=["charge_needed_system_zones_count"])\
#    .plot(column="charge_needed_system_zones_count", ax=ax, legend=True)
#plt.title("system charging locations heatmap")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()
#
#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["charge_needed_users_zones_count"] = \
#    sim_users_charges_bookings.destination_id.value_counts()
#grid.dropna(subset=["charge_needed_users_zones_count"])\
#    .plot(column="charge_needed_users_zones_count", ax=ax, legend=True)
#plt.title("users charging locations heatmap")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()

#plt.figure()
#sim_unsatisfied_requests["hour"].hist\
#    (bins=24, alpha=0.7, density=True,
#          label="system")
#plt.legend()
#plt.title("unsatisfied demand timestamps histogram")
#plt.xlabel("hour")
#plt.show()
#plt.close()
#
#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["unsatisfied_demand_origins_count"] = \
#    sim_unsatisfied_requests.origin_id.value_counts()
#grid.dropna(subset=["unsatisfied_demand_origins_count"])\
#    .plot(column="unsatisfied_demand_origins_count", ax=ax, legend=True)
#plt.title("unsatisfied demand origin heatmap")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()

#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["unsatisfied_demand_origins_count_morning"] = \
#    sim_unsatisfied_requests.loc\
#    [(sim_unsatisfied_requests.hour > 3)\
#     & (sim_unsatisfied_requests.hour < 9)].origin_id.value_counts()
#grid.dropna(subset=["unsatisfied_demand_origins_count_morning"])\
#    .plot(column="unsatisfied_demand_origins_count_morning", ax=ax, legend=True)
#plt.title("unsatisfied demand origin heatmap morning")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()
#
#fig,ax = plt.subplots(1,1,figsize=(15,15))
#grid["unsatisfied_demand_origins_count_afternoon"] = \
#    sim_unsatisfied_requests.loc\
#    [(sim_unsatisfied_requests.hour > 14)\
#     & (sim_unsatisfied_requests.hour < 20)].origin_id.value_counts()
#grid.dropna(subset=["unsatisfied_demand_origins_count_afternoon"])\
#    .plot(column="unsatisfied_demand_origins_count_afternoon", ax=ax, legend=True)
#plt.title("unsatisfied demand origin heatmap afternoon")
#plt.xlabel("longitude")
#plt.ylabel("latitude")
#plt.show()
#plt.close()
