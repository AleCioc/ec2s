import datetime
import numpy as np
import pandas as pd

from Simulation.EFFCS_ChargingPrimitives import get_charging_soc
from utils.car_utils import soc_to_kwh

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
		# print(self.sim_charges)

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
			(sim.chargingStrategy.list_users_charging_bookings,
			 columns = self.sim_system_charges_bookings.columns)

		self.sim_users_charges_bookings["end_hour"] = \
			self.sim_users_charges_bookings["end_time"].apply\
			(lambda d: d.hour)

		self.sim_unfeasible_charge_bookings = pd.DataFrame(
			sim.chargingStrategy.sim_unfeasible_charge_bookings
		)

		self.sim_booking_requests["n_cars_charging_system"] = \
			pd.Series(sim.list_n_cars_charging_system)

		self.sim_booking_requests["n_cars_charging_users"] = \
			pd.Series(sim.list_n_cars_charging_users).fillna(0)

		self.sim_booking_requests["n_cars_available"] = \
			pd.Series(sim.list_n_cars_available)

		self.sim_booking_requests["n_cars_booked"] = \
			pd.Series(sim.list_n_cars_booked)

		self.sim_booking_requests["n_cars_dead"] = \
			pd.Series(sim.list_n_cars_dead)

		self.sim_charge_deaths = \
					pd.DataFrame(sim.chargingStrategy.sim_unfeasible_charge_bookings)

		# Sim Stats creation

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

		self.sim_stats.loc["percentage_satisfied"] = \
			self.sim_stats["n_bookings"] / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_unsatisfied"] = \
			1.0 - self.sim_stats.loc["percentage_satisfied"]

		self.sim_stats.loc["percentage_same_zone_trips"] = \
					self.sim_stats["n_unsatisfied"] / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_same_zone_trips"] = \
			sim.n_same_zone_trips / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_not_same_zone_trips"] = \
			sim.n_not_same_zone_trips / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_no_close_cars"] = \
			sim.n_no_close_cars / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_deaths"] = \
			sim.n_deaths / self.sim_stats["n_booking_reqs"]

		self.sim_stats.loc["percentage_same_zone_trips_satisfied"] = \
			sim.n_same_zone_trips / self.sim_stats["n_bookings"]

		self.sim_stats.loc["percentage_not_same_zone_trips_satisfied"] = \
			sim.n_not_same_zone_trips / self.sim_stats["n_bookings"]

		self.sim_stats.loc["percentage_no_close_cars_unsatisfied"] = \
			sim.n_no_close_cars / self.sim_stats["n_unsatisfied"]

		self.sim_stats.loc["percentage_deaths_unsatisfied"] = \
			sim.n_deaths / self.sim_stats["n_unsatisfied"]

		self.sim_stats.loc["n_charges"] = \
			len(self.sim_charges)

		self.sim_stats.loc["n_charging_requests_system"] = \
			len(self.sim_system_charges_bookings)

		self.sim_stats.loc["n_charges_system"] = \
			self.sim_charges.groupby("operator")\
				.date.count().loc["system"]

		self.sim_stats.loc["n_charge_deaths"] = \
			len(self.sim_charge_deaths)

		self.sim_stats.loc["percentage_charge_deaths"] = \
			len(self.sim_charge_deaths) / self.sim_stats.loc["n_charges"]

		self.sim_stats.loc["percentage_charge_deaths_system"] = \
			len(self.sim_charge_deaths) / self.sim_stats.loc["n_charges_system"]

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

		self.sim_stats["sim_duration"] = (self.sim_stats.sim_end - self.sim_stats.sim_start).total_seconds()

		self.sim_stats.loc["tot_potential_mobility_energy"] = \
			self.sim_booking_requests.soc_delta.sum()

		self.sim_stats.loc["tot_potential_charging_energy"] = \
			get_charging_soc(self.sim_stats["sim_duration"] / 60) * self.sim_stats["n_charging_poles"]

		self.sim_stats.loc["tot_charging_energy"] = \
			self.sim_charges["soc_delta_kwh"].sum()

		self.sim_stats.loc["percentage_charges_system"] = \
			self.sim_charges.groupby("operator")\
			.date.count().loc["system"]\
			/ len(self.sim_charges)

		if "users" in self.sim_charges.operator.unique():
			self.sim_stats.loc["percentage_charges_users"] = \
				self.sim_charges.groupby("operator")\
				.date.count().loc["users"]\
				/ len(self.sim_charges)
		else:
			self.sim_stats.loc["percentage_charges_users"] = 0

		if "users" in self.sim_charges.operator.unique():
			self.sim_stats.loc["percentage_energy_system"] = \
				self.sim_charges.groupby("operator")\
				.soc_delta_kwh.sum().loc["system"]\
				/ self.sim_stats["tot_charging_energy"]
			self.sim_stats.loc["percentage_energy_users"] = \
				self.sim_charges.groupby("operator")\
				.soc_delta_kwh.sum().loc["users"]\
				/ self.sim_stats["tot_charging_energy"]
		else:
			self.sim_stats.loc["percentage_energy_system"] = 1
			self.sim_stats.loc["percentage_energy_users"] = 0

		if len(self.sim_users_charges_bookings):
			self.sim_stats.loc["percentage_duration_system"] = \
				self.sim_charges.groupby("operator")\
				.duration.sum().loc["system"]\
				/ self.sim_charges.duration.sum()
			self.sim_stats.loc["percentage_duration_users"] = \
				self.sim_charges.groupby("operator")\
				.duration.sum().loc["users"]\
				/ self.sim_charges.duration.sum()
		else:
			self.sim_stats.loc["percentage_duration_system"] = 1
			self.sim_stats.loc["percentage_duration_users"] = 0

		self.sim_stats.loc["charging_energy_event_avg"] = \
			self.sim_charges.soc_delta_kwh.mean()

		self.sim_stats.loc["charging_energy_event_max"] = \
			self.sim_charges.soc_delta_kwh.max()

		self.sim_stats.loc["charging_energy_event_med"] = \
			self.sim_charges.soc_delta_kwh.median()

#        stat_names = ["n_charges", "charging_energy"]
#        group_cols = ["date", "day_hour"]
#        stat_ops = ["avg", "max", "med"]
#
#        for group_col in group_cols:
#
#            self.sim_stats.loc["n_charges_by_" + group_col + "_avg"] = \
#                self.sim_charges.groupby(group_col).date.count().mean()
#            self.sim_stats.loc["n_charges_by_" + group_col + "_max"] = \
#                self.sim_charges.groupby(group_col).date.count().max()
#            self.sim_stats.loc["n_charges_by_" + group_col + "_med"] = \
#                self.sim_charges.groupby(group_col).date.count().median()
#
#        for group_col in group_cols:
#
#            self.sim_stats.loc["charging_energy_by_" + group_col + "_avg"] = \
#                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().mean()
#            self.sim_stats.loc["charging_energy_by_" + group_col + "_max"] = \
#                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().max()
#            self.sim_stats.loc["charging_energy_by_" + group_col + "_med"] = \
#                self.sim_charges.groupby(group_col).soc_delta_kwh.sum().median()
#
#        stat_names = ["n_charges", "charging_energy"]
#        resample_freqs = ["60Min", "1440Min", "10080Min"]
#        stat_ops = ["avg", "max", "med"]
#
#        for freq_col in resample_freqs:
#
#            self.sim_stats.loc["n_charges_by_" + freq_col + "_avg"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).date.count().mean()
#            self.sim_stats.loc["n_charges_by_" + freq_col + "_max"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).date.count().max()
#            self.sim_stats.loc["n_charges_by_" + freq_col + "_med"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).date.count().median()
#
#        for freq_col in resample_freqs:
#
#            self.sim_stats.loc["charging_energy_by_" + freq_col + "_avg"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).soc_delta_kwh.sum().mean()
#            self.sim_stats.loc["charging_energy_by_" + freq_col + "_max"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).soc_delta_kwh.sum().max()
#            self.sim_stats.loc["charging_energy_by_" + freq_col + "_med"] = \
#                self.sim_charges.set_index("start_time")\
#                .resample(freq_col).soc_delta_kwh.sum().median()

		self.sim_charges["cr_timeout"] = \
			self.sim_charges.timeout_outward\
			+ self.sim_charges.timeout_return

		self.sim_stats.loc["cum_relo_out_t"] = \
			self.sim_charges.timeout_outward.sum() / 60 / 60

		self.sim_stats.loc["cum_relo_ret_t"] = \
			self.sim_charges.timeout_return.sum() / 60 / 60

		self.sim_stats.loc["cum_relo_t"] = \
			self.sim_stats.cum_relo_out_t + \
			self.sim_stats.cum_relo_ret_t

		self.sim_stats.loc["cum_relo_khw"] = \
			self.sim_charges.cr_soc_delta_kwh.sum()

		self.sim_stats.loc["avg_hourly_relo_t"] = \
			self.sim_charges.groupby("hour").cr_timeout.sum().mean()

		self.sim_stats.loc["total_trips_duration"] = self.sim_bookings.duration.sum()
