import datetime
import numpy as np
import pandas as pd

class EFFCS_SimOutput ():

    def __init__ (self, sim):

#        self.sim_events = \
#            pd.DataFrame(sim.events)
#
#        self.sim_events.columns = [
#                    "ev_time",
#                    "ev_seqno",
#                    "ev_class",
#                ]

        self.sim_booking_requests = \
            pd.DataFrame(sim.sim_booking_requests)

        self.sim_bookings = \
            self.sim_booking_requests.dropna()

        self.sim_charges = \
            pd.DataFrame(sim.chargingStrategy.sim_charges)

        self.sim_deaths = \
            pd.DataFrame(sim.sim_booking_requests_deaths)

        self.sim_unsatisfied_requests = \
            pd.DataFrame(sim.sim_unsatisfied_requests)

        self.sim_system_charges_bookings = \
            pd.DataFrame(sim.chargingStrategy.list_system_charging_bookings)

        self.sim_system_charges_bookings["end_hour"] = \
            self.sim_system_charges_bookings["end_time"].apply\
            (lambda d: d.hour)

        self.sim_users_charges_bookings = pd.DataFrame\
            (sim.chargingStrategy.list_users_charging,
             columns = self.sim_system_charges_bookings.columns)

        self.sim_users_charges_bookings["end_hour"] = \
            self.sim_users_charges_bookings["end_time"].apply\
            (lambda d: d.hour)

        self.sim_booking_requests["n_cars_charging_system"] = \
            pd.Series(sim.list_n_cars_charging_system)

        self.sim_booking_requests["n_cars_charging_users"] = \
            pd.Series(sim.list_n_cars_charging_users).fillna(0)

        self.sim_booking_requests["n_cars_available"] = \
            pd.Series(sim.list_n_cars_available)

        self.sim_booking_requests["n_cars_booked"] = \
            pd.Series(sim.list_n_cars_booked)

        self.sim_stats = \
            pd.Series(name="sim_stats")

        self.sim_stats = pd.concat\
            ([self.sim_stats, 
              pd.Series(sim.simInput.sim_general_conf)])

        self.sim_stats = pd.concat\
            ([self.sim_stats, 
              pd.Series(sim.simInput.sim_scenario_conf)])

        self.sim_stats.loc["n_same_zone_trips"] = \
            sim.n_same_zone_trips

        self.sim_stats.loc["n_not_same_zone_trips"] = \
            sim.n_not_same_zone_trips

        self.sim_stats.loc["n_no_close_cars"] = \
            sim.n_no_close_cars

        self.sim_stats.loc["n_deaths"] = \
            sim.n_deaths

        self.sim_stats["n_booking_reqs"] = \
            self.sim_stats["n_same_zone_trips"]\
            + self.sim_stats["n_not_same_zone_trips"]\
            + self.sim_stats["n_no_close_cars"]\
            + self.sim_stats["n_deaths"]
        
        self.sim_stats["n_bookings"] = \
            self.sim_stats["n_same_zone_trips"]\
            + self.sim_stats["n_not_same_zone_trips"]
        
        self.sim_stats["n_unsatisfied"] = \
            self.sim_stats["n_no_close_cars"]\
            + self.sim_stats["n_deaths"]

        self.sim_stats.loc["n_charges"] = \
            len(self.sim_charges)

        self.sim_stats.loc["soc_avg"] = \
            self.sim_bookings.start_soc.mean()

        self.sim_stats.loc["soc_med"] = \
            self.sim_bookings.start_soc.median()

        self.sim_stats.loc["charging_time_avg"] = \
            self.sim_charges.duration.mean() / 60

        self.sim_stats.loc["charging_time_med"] = \
            self.sim_charges.duration.median() / 60

        self.sim_stats.loc["n_charges_by_car_avg"] = \
            self.sim_charges.groupby("plate").date.count().mean()

        self.sim_stats.loc["n_charges_by_car_system_avg"] = \
            self.sim_charges[self.sim_charges.operator == "system"]\
                .groupby("plate").date.count().mean()

        if len(self.sim_users_charges_bookings):
            self.sim_stats.loc["n_charges_by_car_users_avg"] = \
                self.sim_charges[self.sim_charges.operator == "users"]\
                    .groupby("plate").date.count().mean()
        else:
            self.sim_stats.loc["n_charges_by_car_users_avg"] = 0

        self.sim_stats.loc["tot_energy"] =   \
            self.sim_charges["soc_delta_kwh"].sum()

        self.sim_stats.loc["percentage_charges_system"] = \
            self.sim_charges.groupby("operator")\
            .date.count().loc["system"]\
            / len(self.sim_charges)

        if len(self.sim_users_charges_bookings):
            self.sim_stats.loc["percentage_charges_users"] = \
                self.sim_charges.groupby("operator")\
                .date.count().loc["users"]\
                / len(self.sim_charges)
        else:
            self.sim_stats.loc["percentage_charges_users"] = 0            

        self.sim_stats.loc["charging_energy_event_avg"] = \
            self.sim_charges.soc_delta_kwh.mean()

        self.sim_stats.loc["charging_energy_event_max"] = \
            self.sim_charges.soc_delta_kwh.max()

        self.sim_stats.loc["charging_energy_event_med"] = \
            self.sim_charges.soc_delta_kwh.median()

        stat_names = ["n_charges", "charging_energy"]
        group_cols = ["date", "day_hour"]
        stat_ops = ["avg", "max", "med"]

        for group_col in group_cols:

            self.sim_stats.loc["n_charges_by_" + group_col + "_avg"] = \
                self.sim_charges.groupby(group_col).date.count().mean()
            self.sim_stats.loc["n_charges_by_" + group_col + "_max"] = \
                self.sim_charges.groupby(group_col).date.count().max()
            self.sim_stats.loc["n_charges_by_" + group_col + "_med"] = \
                self.sim_charges.groupby(group_col).date.count().median()

        for group_col in group_cols:

            self.sim_stats.loc["charging_energy_by_" + group_col + "_avg"] = \
                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().mean()
            self.sim_stats.loc["charging_energy_by_" + group_col + "_max"] = \
                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().max()
            self.sim_stats.loc["charging_energy_by_" + group_col + "_med"] = \
                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().median()

        stat_names = ["n_charges", "charging_energy"]
        resample_freqs = ["60Min", "1440Min", "10080Min"]
        stat_ops = ["avg", "max", "med"]

        for freq_col in resample_freqs:

            self.sim_stats.loc["n_charges_by_" + freq_col + "_avg"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).date.count().mean()
            self.sim_stats.loc["n_charges_by_" + freq_col + "_max"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).date.count().max()
            self.sim_stats.loc["n_charges_by_" + freq_col + "_med"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).date.count().median()

        for freq_col in resample_freqs:

            self.sim_stats.loc["charging_energy_by_" + freq_col + "_avg"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).soc_delta_kwh.sum().mean()
            self.sim_stats.loc["charging_energy_by_" + freq_col + "_max"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).soc_delta_kwh.sum().max()
            self.sim_stats.loc["charging_energy_by_" + freq_col + "_med"] = \
                self.sim_charges.set_index("start_time")\
                .resample(freq_col).soc_delta_kwh.sum().median()
