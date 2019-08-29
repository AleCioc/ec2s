import numpy as np
import pandas as pd

import datetime

from Preprocessing.geo_preprocessing import get_gdfs

from Loading.Loader import Loader

from utils.geo_utils import haversine

def get_bookings_parkings (city, months):

    print ("Loading data into RAM ..")
    t0 = datetime.datetime.now()
    loader = Loader(city, months)
    bookings, parkings = loader.read_bookings_parkings()
    t1 = datetime.datetime.now()
    print (t1 - t0)
    
    return bookings, parkings


def get_input_data(city, months, bin_side_length):
    bookings, parkings = get_bookings_parkings(city, months)

    grid, \
    bookings_origins_gdf, \
    bookings_destinations_gdf, \
    parkings_gdf = get_gdfs \
        (city,
         bin_side_length,
         bookings,
         parkings)


    return bookings,\
            parkings,\
            grid,\
            bookings_origins_gdf,\
            bookings_destinations_gdf,\
            parkings_gdf

def create_input_pickles (city, months, bin_side_length):
    
    # bookings,\
    # parkings,\
    # grid,\
    # bookings_origins_gdf,\
    # bookings_destinations_gdf,\
    # parkings_gdf = get_input_data(city, months, bin_side_length)
    #
    # bookings.to_pickle\
    #     ("./Data/" + city + "/bookings.pickle")
    #
    # parkings.to_pickle\
    #     ("./Data/" + city + "/parkings.pickle")
    #
    # grid.to_pickle\
    #     ("./Data/" + city + "/grid.pickle")
    #
    # bookings_origins_gdf.to_pickle\
    #     ("./Data/" + city + "/bookings_origins_gdf.pickle")
    #
    # bookings_destinations_gdf.to_pickle\
    #     ("./Data/" + city + "/bookings_destinations_gdf.pickle")
    #
    # parkings_gdf.to_pickle\
    #     ("./Data/" + city + "/parkings_gdf.pickle")

    bookings, grid = read_sim_input_data(city)
    grid_lat_lon = grid.copy()
    grid_lat_lon.crs = {"init": "epsg:3857"}
    grid_lat_lon = grid_lat_lon.to_crs({"init": "epsg:4326"})
    centroids_tuple = grid_lat_lon.centroid.apply(lambda p: (p.x, p.y))

    print (grid.shape)
    distances = {}
    for i in range(len(centroids_tuple.values)):
        destinations = []
        for j in range(len(centroids_tuple.values)):
            centroid_i = centroids_tuple.values[i]
            centroid_j = centroids_tuple.values[j]
            destinations += [(i,
                              j,
                              centroid_i[0],
                              centroid_i[1],
                              centroid_j[0],
                              centroid_j[1])]
        destinations = pd.Series(destinations)
        destinations_distances = \
            list(destinations.apply(lambda pp: haversine(pp[2], pp[3], pp[4], pp[5])))
        distances[i] = destinations_distances

    od_distances = pd.DataFrame(distances)
    od_distances.to_pickle("./Data/" + city + "/od_distances.pickle")

def read_sim_input_data (city):

    print ("Loading pickles into RAM ..")
    t0 = datetime.datetime.now()
    bookings = pd.read_pickle("./Data/" + city + "/bookings.pickle")
    grid = pd.read_pickle("./Data/" + city + "/grid.pickle")
    t1 = datetime.datetime.now()
    print (t1 - t0)

    return bookings, grid
