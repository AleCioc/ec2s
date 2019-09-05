import os

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

def EFFCS_SimOutputPlotter ():
    
    def __init__ (self, simOutput, city, grid):

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "single_run")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

        self.city = city
        self.grid = grid

        self.sim_booking_requests = \
            simOutput.sim_booking_requests

        self.sim_bookings = \
            simOutput.sim_booking_requests

        self.sim_charges = \
            simOutput.sim_charges

        self.sim_deaths = \
            simOutput.sim_deaths

        self.sim_unsatisfied_requests = \
            simOutput.sim_unsatisfied_requests

        self.sim_system_charges_bookings = \
            simOutput.sim_system_charges_bookings

        self.sim_users_charges_bookings = \
            simOutput.sim_users_charges_bookings

        self.sim_cars_events = pd.concat\
            ([self.sim_bookings, self.sim_charges], ignore_index=True, sort=False)\
            .sort_values("start_time")

        self.sim_charge_deaths = \
            simOutput.sim_charge_deaths

    def plot_charging_duration_hist (self):

        plt.figure()
        self.sim_charges.duration.apply\
           (lambda x: x/60).hist\
           (bins=50, cumulative=False, density=True)
        plt.title("charge duration histogram")
        plt.xlabel("hours")
        plt.show()
        plt.close()

    def plot_n_charges_avg (self):

        plt.figure()
        (sim_charges.sort_values\
           ("start_time").groupby\
           ("hour").date.count() / len(self.sim_charges.date.unique()))\
           .plot(marker="o")
        plt.title("average number of charging events by hour")
        plt.xlabel("hour")
        plt.ylabel("n charges")
        plt.show()
        plt.close()

    def plot_charging_energy_avg (self):

        plt.figure()
        (sim_charges.sort_values\
           ("start_time").groupby\
           ("hour").soc_delta_kwh.sum() / len(self.sim_charges.date.unique()))\
           .plot(marker="o")
        plt.title("average charging energy by hour")
        plt.xlabel("hour")
        plt.ylabel("E [kwh]")
        plt.show()
        plt.close()

    def plot_n_charges_tot (self):

        plt.figure()
        self.sim_system_charges_bookings.set_index\
            ("start_time").resample\
            ("60Min").destination_id.count().plot(label="system")
        if len(self.sim_users_charges_bookings):
            self.sim_users_charges_bookings.set_index\
                ("start_time").resample\
                ("60Min").destination_id.count().plot(label="users")
        plt.title("number of charging events sum by hour in time")
        plt.legend()
        plt.xlabel("t")
        plt.ylabel("n charges")
        plt.show()
        plt.close()

    def plot_tot_energy (self):

        plt.figure()
        self.sim_charges.sort_values\
           ("start_time").groupby\
           ("day_hour").soc_delta_kwh.sum().plot()
        plt.title("charging energy sum by hour in time")
        plt.xlabel("t")
        plt.ylabel("E [kwh]")
        plt.show()
        plt.close()

    def plot_fleet_status (self):

        plt.figure()
        self.sim_booking_requests\
           .set_index("start_time")\
           .n_cars_charging_system\
           .plot(label="system charging", linewidth=2, alpha=0.7)
        self.sim_booking_requests\
           .set_index("start_time")\
           .n_cars_charging_users\
           .plot(label="users charging", linewidth=2, alpha=0.7)
        self.sim_booking_requests\
           .set_index("start_time")\
           .n_cars_booked\
           .plot(label="booked", linewidth=2, alpha=0.7)
        self.sim_booking_requests\
           .set_index("start_time")\
           .n_cars_available\
           .plot(label="available", linewidth=2, alpha=0.7)
        plt.legend()
        plt.title("number of cars charging/available/booked in time")
        plt.xlabel("t")
        plt.ylabel("E [kwh]")
        plt.show()
        plt.close()

    def plot_n_cars_charging (self):

        plt.figure()
        self.sim_booking_requests\
            .set_index("start_time")\
            .n_cars_charging_system\
            .plot(label="system charging", linewidth=2, alpha=0.7)
        self.sim_booking_requests\
            .set_index("start_time")\
            .n_cars_charging_users\
            .plot(label="users charging", linewidth=2, alpha=0.7)
        plt.legend()
        plt.title("number of cars charging in time")
        plt.xlabel("t")
        plt.ylabel("n cars")
        plt.show()
        plt.close()

    def plot_charging_t_hist (self):

        plt.figure()
        self.sim_system_charges_bookings["end_hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="system")
        self.sim_users_charges_bookings["end_hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="users")
        plt.legend()
        plt.title("charging timestamps histogram system vs users")
        plt.xlabel("hour")
        plt.show()
        plt.close()

    def plot_origin_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["origin_count"] = \
           self.sim_booking_requests.origin_id.value_counts()
        self.grid.dropna(subset=["origin_count"])\
           .plot(column="origin_count", ax=ax, legend=True)
        plt.title("origin heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_destinations_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["destination_count"] = \
           self.sim_booking_requests.destination_id.value_counts()
        self.grid.dropna(subset=["destination_count"])\
           .plot(column="destination_count", ax=ax, legend=True)
        plt.title("destination heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_charging_heatmap_system (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        grid["charge_needed_system_zones_count"] = \
           sim_system_charges_bookings.destination_id.value_counts()
        grid.dropna(subset=["charge_needed_system_zones_count"])\
           .plot(column="charge_needed_system_zones_count", ax=ax, legend=True)
        plt.title("system charging locations heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_charging_heatmap_users (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["charge_needed_users_zones_count"] = \
           self.sim_users_charges_bookings.destination_id.value_counts()
        self.grid.dropna(subset=["charge_needed_users_zones_count"])\
           .plot(column="charge_needed_users_zones_count", ax=ax, legend=True)
        plt.title("users charging locations heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_unsatisfied_t_hist (self):

        plt.figure()
        self.sim_unsatisfied_requests["hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="system")
        plt.legend()
        plt.title("unsatisfied demand timestamps histogram")
        plt.xlabel("hour")
        plt.show()
        plt.close()

    def plot_unsatisfied_origins_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["unsatisfied_demand_origins_count"] = \
           self.sim_unsatisfied_requests.origin_id.value_counts()
        self.grid.dropna(subset=["unsatisfied_demand_origins_count"])\
           .plot(column="unsatisfied_demand_origins_count", ax=ax, legend=True)
        plt.title("unsatisfied demand origin heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_unsatisfied_origins_heatmap_morning (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["unsatisfied_demand_origins_count_morning"] = \
           self.sim_unsatisfied_requests.loc\
           [(self.sim_unsatisfied_requests.hour > 3)\
            & (self.sim_unsatisfied_requests.hour < 9)].origin_id.value_counts()
        self.grid.dropna(subset=["unsatisfied_demand_origins_count_morning"])\
           .plot(column="unsatisfied_demand_origins_count_morning", ax=ax, legend=True)
        plt.title("unsatisfied demand origin heatmap morning")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()

    def plot_unsatisfied_origins_heatmap_afternoon (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["unsatisfied_demand_origins_count_afternoon"] = \
           self.sim_unsatisfied_requests.loc\
           [(self.sim_unsatisfied_requests.hour > 14)\
            & (self.sim_unsatisfied_requests.hour < 20)].origin_id.value_counts()
        self.grid.dropna(subset=["unsatisfied_demand_origins_count_afternoon"])\
           .plot(column="unsatisfied_demand_origins_count_afternoon", ax=ax, legend=True)
        plt.title("unsatisfied demand origin heatmap afternoon")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.show()
        plt.close()
