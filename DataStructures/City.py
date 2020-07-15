import os
import datetime
import pytz

import pandas as pd
from sklearn.neighbors import KernelDensity

from utils.bookings_utils import pre_process_time

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data


class City:

	def __init__(self, city_name, sim_general_conf, kde_bw=1):

		self.city_name = city_name
		self.sim_general_conf = sim_general_conf
		self.kde_bw = kde_bw

		self.bookings, self.grid = read_sim_input_data \
			(city_name)
		print(self.grid.zone_id)

		self.input_bookings = self.get_input_bookings_filtered()
		print(self.input_bookings.zone_id)

		self.valid_zones = self.get_valid_zones()
		print(self.valid_zones)

		self.grid = self.grid.loc[self.valid_zones]
		self.grid["new_zone_id"] = range(len(self.grid))
		self.input_bookings[["origin_id", "destination_id"]] = \
			self.input_bookings[["origin_id", "destination_id"]] \
				.astype(int).replace(self.grid.new_zone_id.to_dict())
		self.grid["zone_id"] = self.grid.new_zone_id
		self.grid = self.grid.reset_index()

		self.original_valid_zones = self.valid_zones.copy()
		self.valid_zones = self.grid.index

		self.od_distances = self.get_od_distances()

		self.neighbors, self.neighbors_dict = self.get_neighbors_dicts()

		self.request_rates = self.get_requests_rates()

		self.trip_kdes = self.get_trip_kdes()

	def get_od_distances(self):

		print(self.grid)
		points = self.grid.centroid.geometry
		print(points)
		self.od_distances = points.apply(lambda p: points.distance(p))

		#od_distances.to_pickle(path)

		# cfr. projection distortion
		#self.od_distances = pd.read_pickle(path)

		return self.od_distances

	def get_neighbors_dicts(self):

		print(self.od_distances)
		self.max_dist = self.od_distances.max().max()

		self.neighbors = self.od_distances \
			[self.od_distances < 1050].apply \
			(lambda x: pd.Series \
				(x.sort_values().dropna().iloc[1:].index.values),
			 axis=1)

		self.neighbors_dict = {}
		for zone in self.neighbors.index:
			self.neighbors_dict[int(zone)] = \
				dict(self.neighbors.loc[zone].dropna())

		return self.neighbors, self.neighbors_dict

	def get_input_bookings_filtered(self):

		def filter_bookings_for_simulation(bookings):

			bookings["date"] = \
				bookings.start_time.apply(lambda d: d.date())
			date_hour_count = \
				bookings.groupby("date").hour.apply(lambda h: len(h.unique()))
			bad_data_dates = \
				list(date_hour_count[date_hour_count < 24].index)

			return \
				bookings.loc \
					[(bookings.duration > 3) \
					 & (bookings.duration < 60) \
					 & (bookings.euclidean_distance > 0.5)] \
					.copy()

		self.bookings = \
			filter_bookings_for_simulation(self.bookings)
		self.bookings.loc[:, "ia_timeout"] = \
			(self.bookings.start_time - \
			 self.bookings.start_time.shift()) \
				.apply(lambda x: x.total_seconds())
		self.bookings = self.bookings \
			.loc[self.bookings.ia_timeout >= 0]

		self.bookings["avg_speed"] = \
			(self.bookings["euclidean_distance"]) \
			/ (self.bookings["duration"] / 60)

		self.input_bookings = self.bookings.loc \
			[(self.bookings.start_time \
			  > self.sim_general_conf["model_start"]) \
			 & (self.bookings.start_time \
			    < self.sim_general_conf["model_end"])].copy()

		if self.city_name == "Vancouver":
			tz = pytz.timezone("America/Vancouver")

		elif self.city_name == "New_York_City":
			tz = pytz.timezone("America/New_York")

		else:
			tz = pytz.timezone("Europe/Rome")
			return self.input_bookings

		now_utc = datetime.datetime.utcnow()
		now_local = pytz.utc.localize(now_utc, is_dst=None).astimezone(tz)
		self.input_bookings.start_time = \
			self.input_bookings.start_time + now_local.utcoffset()
		self.input_bookings.end_time = \
			self.input_bookings.end_time + now_local.utcoffset()
		self.input_bookings = pre_process_time(self.input_bookings)

		return self.input_bookings

	def get_hourly_ods(self):

		self.hourly_ods = {}

		for hour, hour_df \
				in self.input_bookings.groupby("hour"):
			self.hourly_ods[hour] = pd.DataFrame(
				index=self.valid_zones,
				columns=self.valid_zones
			)
			hourly_od = pd.pivot_table(
				hour_df,
				values="start_time",
				index="origin_id",
				columns="destination_id",
				aggfunc=len,
				fill_value=0
			)
			self.hourly_ods[hour].loc\
				[hourly_od.index, hourly_od.columns] = hourly_od
			self.hourly_ods[hour].fillna(0, inplace=True)

	def get_requests_rates(self):

		self.request_rates = {}

		for daytype, daytype_bookings_gdf \
				in self.input_bookings.groupby("daytype"):
			self.request_rates[daytype] = {}
			for hour, hour_df \
					in daytype_bookings_gdf.groupby("hour"):
				self.request_rates[daytype][hour] = \
					hour_df.city.count() \
					/ (len(hour_df.day.unique())) \
					/ 3600

		self.sim_general_conf["avg_request_rate"] = \
			pd.DataFrame(self.request_rates.values()).mean().mean()

		return self.request_rates

	def get_trip_kdes(self):

		self.trip_kdes = {}
		self.kde_columns = [
			"origin_id",
			"destination_id",
			# "duration"
		]

		for daytype, daytype_bookings_gdf \
				in self.input_bookings.groupby("daytype"):
			self.trip_kdes[daytype] = {}
			for hour, hour_df \
					in daytype_bookings_gdf.groupby("hour"):
				self.trip_kdes[daytype][hour] = \
					KernelDensity(
						bandwidth=self.kde_bw
					).fit(hour_df[self.kde_columns].dropna())

		return self.trip_kdes

	def get_valid_zones(self):

		origin_zones_count = \
			self.input_bookings.origin_id.value_counts()
		dest_zones_count = \
			self.input_bookings.destination_id.value_counts()
		self.zones_count = pd.concat \
			([origin_zones_count, dest_zones_count], axis=1)
		valid_origin_zones = origin_zones_count \
			[(origin_zones_count > 10)]
		valid_dest_zones = dest_zones_count \
			[(dest_zones_count > 10)]
		self.valid_zones = valid_origin_zones.index \
			.intersection(valid_dest_zones.index) \
			.astype(int)

		self.input_bookings = self.input_bookings.loc \
			[(self.input_bookings.origin_id.isin(self.valid_zones)) \
			 & (self.input_bookings.destination_id.isin(self.valid_zones))]

		return self.valid_zones
