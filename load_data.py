import datetime

from geo_preprocessing import get_gdfs

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

    return bookings,\
            parkings,\
            grid,\
            bookings_origins_gdf,\
            bookings_destinations_gdf,\
            parkings_gdf            
