import os

import pandas as pd

from DataStructures.City import City

from SimulationInput.confs.sim_general_conf import sim_general_conf

for city in [
				"Berlin",
			]:

	sim_general_conf["city"] = city
	sim_general_conf["bin_side_length"] = 500

	city_obj = City \
		(city,
		 sim_general_conf)

	city_obj.get_hourly_ods()
	writer = pd.ExcelWriter(os.path.join("Data", city, 'hourly_ods.xlsx'), engine ='xlsxwriter')
	for hour in range(24):
		city_obj.hourly_ods[hour].to_excel(writer, sheet_name=str(hour))
	writer.save()
	writer.close()

	city_obj.od_distances.to_csv\
		(os.path.join("Data", city, 'od_distances.csv'))
