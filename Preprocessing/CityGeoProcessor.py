import geopandas as gpd

from utils.geo_utils import get_bookings_gdf
from utils.geo_utils import get_parkings_gdf
from utils.geo_utils import get_city_grid

class CityGeoProcessor ():
    
    def __init__ (self, city, bookings, parkings):
        
        self.city = city
        self.bookings = bookings
        self.parkings = parkings

    def dfs_to_gdfs (self):

        self.bookings_origins_gdf = get_bookings_gdf\
            (self.bookings.copy(), ["start_longitude", "start_latitude"])

        self.bookings_destinations_gdf = get_bookings_gdf\
            (self.bookings.copy(), ["end_longitude", "end_latitude"])

        self.parkings_gdf = get_parkings_gdf\
            (self.parkings.copy())
        
        self.bookings["euclidean_distance"] = \
            self.bookings_origins_gdf.distance\
                (self.bookings_destinations_gdf) / 1000
        
        return self.bookings_origins_gdf,\
                self.bookings_destinations_gdf,\
                self.parkings_gdf

    def apply_binning (self, bin_side_length):

        # 0.7 factor correction needed for Mercator projections
        # Is it the same factor for every latitude?
        self.bin_side_length = bin_side_length / 0.7
        self.grid = get_city_grid\
            (self.parkings_gdf, self.bin_side_length)
            
        return self.grid

    def map_points_to_city_grid (self):
        
        self.bookings_origins_gdf =  gpd.sjoin\
            (self.bookings_origins_gdf, 
             self.grid.drop("zone_id", axis=1), 
             how='left', 
             op='within').rename\
                 ({"index_right": "origin_id"}, axis=1)

        self.bookings_destinations_gdf =  gpd.sjoin\
            (self.bookings_destinations_gdf, 
             self.grid.drop("zone_id", axis=1), 
             how='left', 
             op='within').rename\
                 ({"index_right": "destination_id"}, axis=1)

        self.parkings_gdf =  gpd.sjoin\
            (self.parkings_gdf, 
             self.grid.drop("zone_id", axis=1), 
             how='left', 
             op='within').rename\
                 ({"index_right": "zone_id"}, axis=1)

        self.bookings["origin_id"] = \
            self.bookings_origins_gdf.origin_id\
            .dropna().astype(int)

        self.bookings["destination_id"] = \
            self.bookings_destinations_gdf.destination_id\
            .dropna().astype(int)

        self.parkings["zone_id"] = \
            self.parkings_gdf.zone_id\
            .dropna().astype(int)

        return self.bookings_origins_gdf,\
                self.bookings_destinations_gdf,\
                self.parkings_gdf
