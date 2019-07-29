import sys

import pandas as pd

import datetime

from Preprocessing.geo_preprocessing import get_gdfs

from Loading.Loader import Loader

def get_bookings_parkings (city, months):

    print ("Loading data into RAM ..")
    t0 = datetime.datetime.now()
    loader = Loader(city, months)
    bookings, parkings = loader.read_bookings_parkings()
    t1 = datetime.datetime.now()
    print (t1 - t0)
    
    return bookings, parkings

def get_input_data (city, months, bin_side_length):
    
    bookings, parkings = get_bookings_parkings(city, months)
    
    grid,\
    bookings_origins_gdf,\
    bookings_destinations_gdf,\
    parkings_gdf = get_gdfs\
        (city,
         bin_side_length,
         bookings,
         parkings)
        
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

    od_distances = grid.centroid.apply\
        (lambda x: grid.centroid.distance(x))
    od_distances.to_pickle("./Data/" + city + "/od_distances.pickle")

    return bookings,\
            parkings,\
            grid,\
            bookings_origins_gdf,\
            bookings_destinations_gdf,\
            parkings_gdf            

def read_sim_input_data (city):

    print ("Loading pickles into RAM ..")
    t0 = datetime.datetime.now()
    bookings = pd.read_pickle("./Data/" + city + "/bookings.pickle")
    grid = pd.read_pickle("./Data/" + city + "/grid.pickle")
    t1 = datetime.datetime.now()
    print (t1 - t0)

    return bookings, grid
