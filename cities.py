import os

import pandas as pd

from DataStructures.City import City

from SimulationInput.confs.sim_general_conf import sim_general_conf

for city in [
				"Milano",
				"Berlin",
			]:

	sim_general_conf["city"] = city
	sim_general_conf["bin_side_length"] = 500

	city_obj = City \
		(city,
		 sim_general_conf)

	# city_obj.get_hourly_ods()
	# writer = pd.ExcelWriter(os.path.join("Data", city, 'hourly_ods.xlsx'), engine ='xlsxwriter')
	# for hour in range(24):
	# 	od = city_obj.hourly_ods[hour]
	# 	od = od.loc[city_obj.valid_zones, city_obj.valid_zones]
	# 	od.to_excel(writer, sheet_name=str(hour))
	# writer.save()
	# writer.close()

	# od_dist = city_obj.od_distances
	# od_dist = \
	# 	od_dist.loc[city_obj.valid_zones, city_obj.valid_zones]
	# od_dist.to_csv\
	# 	(os.path.join("Data", city, 'od_distances.csv'))

	# grid = city_obj.grid
	# grid = \
	# 	grid.loc[city_obj.valid_zones]
	# grid.to_csv\
	# 	(os.path.join("Data", city, 'grid.csv'))

	city_obj.bookings.set_index("start_time").resample("1440Min")\
		.plate.apply(lambda x: len(x.unique()))\
		.to_csv((os.path.join("Data", city, 'n_cars.csv')))