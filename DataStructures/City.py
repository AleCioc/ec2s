import pandas as pd
from sklearn.neighbors import KernelDensity

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

class City ():
    
    def __init__ (self, city_name, sim_general_conf):
            
        self.city_name = city_name
        self.sim_general_conf = sim_general_conf
        self.bookings, self.grid = read_sim_input_data\
            (city_name)
        self.neighbors, self.neighbors_dict = self.get_neighbors_dicts()
        self.input_bookings = self.get_input_bookings_filtered()
        self.request_rates = self.get_requests_rates()
        self.trip_kdes = self.get_trip_kdes()
        self.valid_zones = self.get_valid_zones()

    def get_neighbors_dicts (self):

#        self.od_distances = self.grid.centroid.apply\
#            (lambda x: self.grid.centroid.distance(x))
#        self.od_distances.to_pickle("./Data/" + self.city + "/od_distances.pickle")

        self.od_distances = pd.read_pickle\
            ("./Data/" + self.city_name + "/od_distances.pickle")
        self.max_dist = self.od_distances.max().max()

        self.neighbors = self.od_distances\
            [self.od_distances < 1000].apply\
            (lambda x: pd.Series\
             (x.sort_values().dropna().iloc[1:].index.values),
             axis=1)

        self.neighbors_dict = {}
        for zone in self.neighbors.index:
            self.neighbors_dict[int(zone)] = \
                dict(self.neighbors.loc[zone].dropna())
                
        return self.neighbors,\
                self.neighbors_dict

    def get_input_bookings_filtered (self):

        def filter_bookings_for_simulation (bookings):
        
            return \
                bookings.loc\
                [(bookings.duration > 3)\
                 &(bookings.duration < 60)\
                 &(bookings.euclidean_distance > 0.5)]\
                 .copy()        

        self.bookings = \
            filter_bookings_for_simulation(self.bookings)
        self.bookings.loc[:, "ia_timeout"] = \
            (self.bookings.start_time - \
             self.bookings.start_time.shift())\
            .apply(lambda x: x.total_seconds())
        self.bookings = self.bookings\
            .loc[self.bookings.ia_timeout >= 0]

        self.bookings["avg_speed"] = \
            (self.bookings["euclidean_distance"])\
            / (self.bookings["duration"] / 60)

        self.input_bookings = self.bookings.loc\
            [(self.bookings.start_time\
              > self.sim_general_conf["model_start"])\
             & (self.bookings.start_time\
              < self.sim_general_conf["model_end"])].copy()

        return self.input_bookings

    def get_requests_rates (self):

        self.request_rates = {}

        for daytype, daytype_bookings_gdf \
        in self.input_bookings.groupby("daytype"):
            self.request_rates[daytype] = {}  
            for hour, hour_df\
            in daytype_bookings_gdf.groupby("hour"):
                self.request_rates[daytype][hour] = \
                    hour_df.city.count()\
                    / (len(hour_df.day.unique()))\
                    / 3600

        self.sim_general_conf["avg_request_rate"] = \
            pd.DataFrame(self.request_rates.values()).mean().mean()

        return self.request_rates

    def get_trip_kdes (self):

        self.trip_kdes = {}        
        self.kde_columns = [
            "origin_id", 
            "destination_id",
            "duration"        
        ]
        
        for daytype, daytype_bookings_gdf\
        in self.input_bookings.groupby("daytype"):
            self.trip_kdes[daytype] = {}
            for hour, hour_df\
            in daytype_bookings_gdf.groupby("hour"):
                self.trip_kdes[daytype][hour] = \
                    KernelDensity(
                            bandwidth=0.01
                        ).fit(\
                        hour_df[self.kde_columns].dropna())
                    
        return self.trip_kdes

    def get_valid_zones (self):

        origin_zones_count = \
            self.input_bookings.origin_id.value_counts()
        dest_zones_count = \
            self.input_bookings.destination_id.value_counts()
        self.zones_count = pd.concat\
            ([origin_zones_count, dest_zones_count], axis=1)
        valid_origin_zones = origin_zones_count\
            [(origin_zones_count > 0)]
        valid_dest_zones = dest_zones_count\
            [(dest_zones_count > 0)]
        self.valid_zones = valid_origin_zones.index\
            .intersection(valid_dest_zones.index)\
            .astype(int)

        return self.valid_zones
