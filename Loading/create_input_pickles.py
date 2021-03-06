import os
import datetime

import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from DataStructures.City import City
from SimulationInput.confs.sim_general_conf import sim_general_conf

def create_input_pickles(city, months, bin_side_length):

    print(datetime.datetime.now())

    path = os.path.join("Data", city, "bookings.pickle")
    if not os.path.exists(path):

        bookings,\
        parkings,\
        grid,\
        bookings_origins_gdf,\
        bookings_destinations_gdf,\
        parkings_gdf = get_input_data(city, months, bin_side_length)

        bookings.to_pickle\
            ("./Data/" + city + "/bookings.pickle")

        parkings.to_pickle\
            ("./Data/" + city + "/parkings.pickle")

        grid.to_pickle\
            ("./Data/" + city + "/grid.pickle")

        bookings_origins_gdf.to_pickle\
            ("./Data/" + city + "/bookings_origins_gdf.pickle")

        bookings_destinations_gdf.to_pickle\
            ("./Data/" + city + "/bookings_destinations_gdf.pickle")

        parkings_gdf.to_pickle\
            ("./Data/" + city + "/parkings_gdf.pickle")

    path = os.path.join("Data", city, "od_distances.pickle")
    if not os.path.exists(path):

        print(datetime.datetime.now())
        # contains od_distances creation
        city_obj = City \
            (city,
             sim_general_conf)
        print(datetime.datetime.now())