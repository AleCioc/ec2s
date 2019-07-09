import datetime

from Preprocessing.CityGeoProcessor import CityGeoProcessor

def get_gdfs (city, bin_side_length, bookings, parkings):

    geoProcessor = CityGeoProcessor(city, bookings, parkings)

    print ("Getting GeoDataFrames from DataFrames ..")
    t0 = datetime.datetime.now()
    bookings_origins_gdf,\
    bookings_destinations_gdf,\
    parkings_gdf = geoProcessor.dfs_to_gdfs()
    t1 = datetime.datetime.now()
    print (t1 - t0)

    print ("Binning city surface ..")    
    t0 = datetime.datetime.now()
    grid = geoProcessor.apply_binning(bin_side_length)
    t1 = datetime.datetime.now()
    print (t1 - t0)

    print ("Mapping points to bins ..")
    t0 = datetime.datetime.now()
    bookings_origins_gdf,\
    bookings_destinations_gdf,\
    parkings_gdf = geoProcessor.map_points_to_city_grid()
    t1 = datetime.datetime.now()
    print (t1 - t0)

    return grid, \
            bookings_origins_gdf, \
            bookings_destinations_gdf, \
            parkings_gdf