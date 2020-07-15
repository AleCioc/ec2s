import os
import pandas as pd

from Preprocessing.geo_preprocessing import get_gdfs

from Loading.Loader import Loader

def get_bookings_parkings (city, months):

    loader = Loader(city, months)
    bookings, parkings = loader.read_bookings_parkings()
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

def read_sim_input_data (city):

    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "Data",
        city,
        "bookings.pickle"
    )
    bookings = pd.read_pickle(path)
    print(bookings)
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "Data",
        city,
        "grid.pickle"
    )
    grid = pd.read_pickle(path)
    return bookings, grid
