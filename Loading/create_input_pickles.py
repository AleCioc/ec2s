import sys

from Loading.load_data import get_input_data

city_name = sys.argv[1]
bookings,\
parkings,\
grid,\
bookings_origins_gdf,\
bookings_destinations_gdf,\
parkings_gdf = get_input_data\
    (city_name, [9, 10], 500)
