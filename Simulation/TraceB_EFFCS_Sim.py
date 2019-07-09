from utils.car_utils import *
from Simulation.EFFCS_Sim import EFFCS_Sim

class TraceB_EFFCS_Sim (EFFCS_Sim):

    def update_req_time_info (self, booking_request):

        booking_request["date"] = \
            booking_request["start_time"].date()
        booking_request["hour"] = \
            booking_request["start_time"].hour
        booking_request["weekday"] = \
            booking_request["start_time"].weekday()
        if booking_request["weekday"] in [5, 6]:
            booking_request["daytype"] = "weekend"
        else:
            booking_request["daytype"] = "weekday"
        return booking_request

    def fuel_to_electric (self, booking_request):

        booking_request["euclidean_distance_trace"] = \
            booking_request["euclidean_distance"]            

        booking_request["soc_delta_trace"] = \
            -get_soc_delta(booking_request["euclidean_distance_trace"])

        booking_request["euclidean_distance"] = \
            self.od_distances.loc\
            [booking_request["origin_id"], 
             booking_request["destination_id"]] / 1000

        booking_request["soc_delta"] = \
            -get_soc_delta(booking_request["euclidean_distance"])

        booking_request["soc_delta_kwh"] = \
            soc_to_kwh(booking_request["soc_delta"])        

        return booking_request
    
    def mobility_requests_generator(self):

        self.od_distances = self.simInput.od_distances

        for booking_request in self.simInput.booking_requests_list:
            booking_request = self.update_req_time_info(booking_request)
            booking_request = self.fuel_to_electric(booking_request)
            yield self.env.timeout\
                (booking_request["ia_timeout"])
            self.process_booking_request(booking_request)
