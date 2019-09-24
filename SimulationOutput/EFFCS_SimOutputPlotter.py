import os

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

class EFFCS_SimOutputPlotter ():
    
    def __init__ (self, simOutput, city, grid, sim_scenario_name = "trial"):

        self.city = city

        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, "single_run")
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)
        self.figures_path = os.path.join\
            (os.getcwd(), "Figures", self.city, "single_run", sim_scenario_name)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)

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

        self.simOutput = simOutput

        if sim_scenario_name == "only_hub":

            fig, ax = plt.subplots(1, 1, figsize=(15, 15))
            plt.title("Location of hub")
            grid.plot(color="white", edgecolor="black", ax=ax)
            grid.plot \
                (color="lavender", edgecolor="blue", column="valid", ax=ax).plot()
            grid.iloc[self.simOutput.sim_stats["hub_zone"]:self.simOutput.sim_stats["hub_zone"]+1]\
                .plot(ax=ax)
            plt.savefig(os.path.join(self.figures_path,
                 "hub_location.pdf"))

        if sim_scenario_name == "only_cps":

            charging_zones = \
                pd.Index(self.sim_users_charges_bookings\
                .destination_id.unique())
            charging_poles_by_zone = \
                self.sim_users_charges_bookings \
                .destination_id.value_counts()
            grid.loc[charging_zones, "poles_count"] = \
                charging_poles_by_zone
            print (grid.poles_count)

            fig, ax = plt.subplots(1, 1, figsize=(15, 15))
            plt.title("Location of charging poles")
            grid.plot(color="white", edgecolor="black", ax=ax)
            grid.plot \
                (color="lavender", edgecolor="blue", column="valid", ax=ax).plot()
            grid.loc[charging_zones].plot(ax=ax)
            # grid.dropna().plot(column="poles_count", ax=ax, legend=True)
            plt.savefig(os.path.join(self.figures_path,
                 "cps_locations.pdf"))

    def plot_events_profile (self):

        fig, ax = plt.subplots(figsize=(15, 7))
        plt.title("Percentage of events, single simulation")
        pd.DataFrame([
            pd.Series( \
                [self.simOutput.sim_stats["percentage_same_zone_trips_satisfied"],
                 self.simOutput.sim_stats["percentage_not_same_zone_trips_satisfied"]],
                index=["same zone", "neighbor zone"],
                name="satisfied %"),
            pd.Series( \
                [self.simOutput.sim_stats["percentage_no_close_cars_unsatisfied"],
                 self.simOutput.sim_stats["percentage_deaths_unsatisfied"]],
                index=["no close car", "not enough energy"],
                name="unsatisfied %"),
            pd.Series( \
                [self.simOutput.sim_stats["percentage_unsatisfied"],
                 self.simOutput.sim_stats["percentage_satisfied"]],
                index=["unsatisfied", "satified"],
                name="events %"),

        ]).plot.barh(stacked=True, ax=ax)

        plt.tight_layout()
        plt.savefig(os.path.join(self.figures_path,
             "events_profile.pdf"))
        # plt.show()
        plt.close()

    def plot_hourly_events_boxplot (self, which_df):

        if which_df == "unsatisfied":
            df = self.sim_unsatisfied_requests
        if which_df == "charges":
            df = self.sim_charges

        table = df.pivot_table\
            (index=["date"], columns=["hour"], aggfunc=len)\
            .fillna(0.0).loc[:, "start_time"]

        # print(table)

        plt.figure()
        table.reset_index().boxplot(column=list(table.columns))
        plt.title(which_df + " hourly boxplot")
        plt.xlabel("hour")
        plt.ylabel("n events")
        plt.savefig(os.path.join\
            (self.figures_path, which_df + "_hourly_boxplot.pdf"))
        # plt.show()
        plt.close()

    def plot_hourly_charging_boxplot (self, operator="system"):

        if operator == "system":
            values_col = "n_cars_charging_system"
        elif operator == "users":
            values_col = "n_cars_charging_users"

        table = self.sim_booking_requests.pivot_table\
            (index=["date"], columns=["hour"], values=[values_col], aggfunc=np.mean)\
            .fillna(0.0).loc[:, values_col]

        # print(table)

        plt.figure()
        table.reset_index().boxplot(column=list(table.columns))
        plt.title("n cars charging hourly boxplot")
        plt.xlabel("hour")
        plt.ylabel("n cars")
        plt.savefig(os.path.join\
            (self.figures_path, "n_cars_charging_" + operator + "_hourly_boxplot.pdf"))
        # plt.show()
        plt.close()

    def plot_hourly_relocost_boxplot (self):

        table = self.sim_charges.pivot_table\
            (index=["date"], columns=["hour"], values=["timeout_outward"], aggfunc=np.sum)\
            .fillna(0.0).loc[:, "timeout_outward"] / 3600

        # print(table)

        plt.figure()
        table.reset_index().boxplot(column=list(table.columns))
        plt.title("relocation cost hourly boxplot")
        plt.xlabel("hour")
        plt.ylabel("relocation cost [hours]")
        plt.savefig(os.path.join\
            (self.figures_path, "relocost_hourly_boxplot.pdf"))
        # plt.show()
        plt.close()

    def plot_charging_duration_hist (self):

        plt.figure()
        self.sim_charges.duration.apply\
           (lambda x: x/60).hist\
           (bins=50, cumulative=False, density=True)
        plt.title("charge duration histogram")
        plt.xlabel("hours")
        plt.savefig(os.path.join(self.figures_path,
             "duration_hist.pdf"))
        # plt.show()
        plt.close()

    def plot_charging_energy_avg (self):

        plt.figure()
        (self.sim_charges.sort_values\
           ("start_time").groupby\
           ("hour").soc_delta_kwh.sum() / len(self.sim_charges.date.unique()))\
           .plot(marker="o")
        plt.title("average charging energy by hour")
        plt.xlabel("hour")
        plt.ylabel("E [kwh]")
        plt.savefig(os.path.join(self.figures_path,
             "avg_charging_energy.pdf"))
        # plt.show()
        plt.close()

    def plot_tot_energy (self):

        plt.figure()
        self.sim_charges.sort_values\
           ("start_time").groupby\
           ("day_hour").soc_delta_kwh.sum().plot()
        plt.title("charging energy sum by hour in time")
        plt.xlabel("t")
        plt.ylabel("E [kwh]")
        plt.savefig(os.path.join(self.figures_path,
             "charging_energy_t.pdf"))
        # plt.show()
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

        self.sim_booking_requests\
           .set_index("start_time")\
           .n_cars_dead\
           .plot(label="dead", linewidth=2, alpha=0.7)

        plt.legend()
        plt.title("number of cars charging/available/booked in time")
        plt.xlabel("t")
        plt.ylabel("E [kwh]")
        plt.savefig(os.path.join(self.figures_path,
             "n_cars_profile.pdf"))
        # plt.show()
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
        plt.savefig(os.path.join(self.figures_path,
             "n_cars_charging_t.pdf"))
        # plt.show()
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
        plt.savefig(os.path.join(self.figures_path,
             "charging_t_hist.pdf"))
        # plt.show()
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
        plt.savefig(os.path.join(self.figures_path,
             "origins_map.pdf"))
        # plt.show()
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
        plt.savefig(os.path.join(self.figures_path,
             "destinations_map.pdf"))
        # plt.show()
        plt.close()

    def plot_charging_needed_heatmap_system (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["charge_needed_system_zones_count"] = \
           self.sim_system_charges_bookings.destination_id.value_counts()\
           / len(self.sim_system_charges_bookings)
        self.grid.dropna(subset=["charge_needed_system_zones_count"])\
           .plot(column="charge_needed_system_zones_count", ax=ax, legend=True)
        plt.title("system charging needed locations heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.savefig(os.path.join(self.figures_path,
             "system_charges_map.pdf"))
        # plt.show()
        plt.close()

    def plot_charging_needed_heatmap_users (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["charge_needed_users_zones_count"] = \
           self.sim_users_charges_bookings.destination_id.value_counts()
        self.grid.dropna(subset=["charge_needed_users_zones_count"])\
           .plot(column="charge_needed_users_zones_count", ax=ax, legend=True)
        plt.title("users charging needed locations heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.savefig(os.path.join(self.figures_path,
             "users_charges_map.pdf"))
        # plt.show()
        plt.close()

    def plot_unsatisfied_t_hist (self):

        plt.figure()
        self.sim_unsatisfied_requests["hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="system")
        plt.legend()
        plt.title("unsatisfied demand timestamps histogram")
        plt.xlabel("hour")
        plt.savefig(os.path.join(self.figures_path,
             "unsatisfied_t_hist.pdf"))
        # plt.show()
        plt.close()

    def plot_unsatisfied_origins_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["unsatisfied_demand_origins_count"] = \
           self.sim_unsatisfied_requests.origin_id.value_counts()\
           / len(self.sim_unsatisfied_requests)
        self.grid.dropna(subset=["unsatisfied_demand_origins_count"])\
           .plot(column="unsatisfied_demand_origins_count", ax=ax, legend=True)
        plt.title("unsatisfied demand origins heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.savefig(os.path.join(self.figures_path,
             "unsatisfied_origins_heatmap.pdf"))
        # plt.show()
        plt.close()

    def plot_deaths_t_hist (self):

        plt.figure()
        self.sim_deaths["hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="system")
        plt.legend()
        plt.title("deaths timestamps histogram")
        plt.xlabel("hour")
        plt.savefig(os.path.join(self.figures_path,
             "deaths_t_hist.pdf"))
        # plt.show()
        plt.close()

    def plot_deaths_origins_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["deaths_origins_count"] = \
           self.sim_deaths.origin_id.value_counts()
        self.grid.dropna(subset=["deaths_origins_count"])\
           .plot(column="deaths_origins_count", ax=ax, legend=True)
        plt.title("deaths origin heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.savefig(os.path.join(self.figures_path,
             "deaths_origins_heatmap.pdf"))
        # plt.show()
        plt.close()

    def plot_charge_deaths_t_hist (self):

        plt.figure()
        self.sim_charge_deaths["hour"].hist\
           (bins=24, alpha=0.7, density=True,
                 label="system")
        plt.legend()
        plt.title("charge deaths timestamps histogram")
        plt.xlabel("hour")
        plt.savefig(os.path.join(self.figures_path,
             "charge_deaths_t_hist.pdf"))
        # plt.show()
        plt.close()

    def plot_charge_deaths_origins_heatmap (self):

        fig,ax = plt.subplots(1,1,figsize=(15,15))
        self.grid["charge_deaths_origins_count"] = \
           self.sim_charge_deaths.origin_id.value_counts()
        self.grid.dropna(subset=["charge_deaths_origins_count"])\
           .plot(column="deaths_origins_count", ax=ax, legend=True)
        plt.title("charge deaths origin heatmap")
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        plt.savefig(os.path.join(self.figures_path,
             "charge_deaths_origins_heatmap.pdf"))
        # plt.show()
        plt.close()

    def plot_relo_cost_t (self):

        plt.figure(figsize=(15, 7))
        self.sim_charges \
            .set_index("start_time") \
            .timeout_outward.apply(lambda x: x / 3600).resample("60Min").sum() \
            .plot(label="relocation hours", linewidth=2, alpha=0.7)
        plt.legend()
        plt.title("Relocation hours needed every 60 minutes")
        plt.xlabel("t")
        plt.ylabel("relocation hours")
        plt.savefig(os.path.join(self.figures_path,
             "relo_cost_t.pdf"))
        # plt.show()
        plt.close()
