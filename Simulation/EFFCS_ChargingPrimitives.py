import datetime

import numpy as np

from utils.car_utils import soc_to_kwh
from utils.car_utils import get_soc_delta

def get_charging_time (soc_delta,
                       battery_capacity = 16.7,
                       charging_efficiency = 0.92,
                       charger_rated_power = 2):

    return (soc_delta * 60 * battery_capacity)\
    / (charging_efficiency * charger_rated_power * 100)

def init_charge (booking_request, cars_soc_dict, car, beta):

    charge = {}
    charge["plate"] = car
    charge["start_time"] = \
        booking_request["end_time"]
    charge["date"] = charge["start_time"].date()
    charge["hour"] = charge["start_time"].hour
    charge["day_hour"] = \
        charge["start_time"].replace(minute=0, second=0, microsecond=0)
    charge["start_soc"] = cars_soc_dict[car]
    charge["end_soc"] = beta
    charge["soc_delta"] = charge["end_soc"] - charge["start_soc"]
    charge["soc_delta_kwh"] = soc_to_kwh(charge["soc_delta"])
    charge["duration"] = \
        (get_charging_time(beta - charge["start_soc"]))

    return charge

def check_system_charge_ (booking_request,
                            cars_soc_dict,
                            car,
                            alpha=25, beta=100):

    if cars_soc_dict[car] < alpha:
        charge = init_charge\
            (booking_request, 
             cars_soc_dict, 
             car,
             beta)
        return True, charge
    else:
        return False, None

def check_user_charge_ (booking_request,
                        cars_soc_dict,
                        car,
                        charging_poles_dict,
                        beta=100, w=0.99):

    destination_id = booking_request["destination_id"]
    if destination_id in charging_poles_dict.keys():
        if np.random.binomial(1, w):
            charge = init_charge\
                (booking_request, 
				 cars_soc_dict, 
				 car,
                 beta)
            return True, charge
        else:
            return False, None
    else:
        return False, None

class EFFCS_ChargingPrimitives ():

    def charge_car (self, 
                    charge, 
                    resource, 
                    car, 
                    operator,
                    zone_id,
                    timeout_outward = 0,
                    timeout_return = 0,
                    cr_soc_delta = 0
                    ):

        charge["operator"] = operator
        charge["zone_id"] = zone_id

        def check_queuing ():
            if self.simInput.sim_scenario_conf["queuing"]:
                return True
            else:
                if resource.count < resource.capacity:
                    return True
                else:
                    return False

        if operator == "system":
            if check_queuing():
                yield self.env.timeout(timeout_outward)
                self.sim_charges += [charge]
                with resource.request() as charging_request:
                    yield charging_request
                    self.n_cars_charging_system += 1
                    yield self.env.timeout(charge["duration"] * 60)
                self.cars_soc_dict[car] = charge["end_soc"]
                self.n_cars_charging_system -= 1
                yield self.env.timeout(timeout_return)

        elif operator == "users":
            if resource.count < resource.capacity:    
                self.sim_charges += [charge]
                with resource.request() as charging_request:
                    yield charging_request
                    self.n_cars_charging_users += 1
                    yield self.env.timeout(charge["duration"] * 60)
                self.cars_soc_dict[car] = charge["end_soc"]
                self.n_cars_charging_users -= 1

        charge["end_time"] = charge["start_time"] + \
            datetime.timedelta(seconds = charge["duration"] * 60)

    def check_system_charge (self, booking_request, car):

        return check_system_charge_\
            (booking_request, 
             self.cars_soc_dict, 
             car, 
             self.simInput.sim_scenario_conf["alpha"],
             self.simInput.sim_scenario_conf["beta"])

    def check_user_charge (self, booking_request, car):

        return check_user_charge_\
            (booking_request, 
             self.cars_soc_dict, 
             car, 
             self.charging_poles_dict,
             self.simInput.sim_scenario_conf["alpha"],
             self.simInput.sim_scenario_conf["willingness"])
    
    def get_timeout (self, origin_id, destination_id):

        distance = self.simInput.od_distances.loc\
            [origin_id, destination_id] / 1000

        return distance / 15 * 3600

    def get_cr_soc_delta (self, origin_id, destination_id):

        distance = self.simInput.od_distances.loc\
            [origin_id, destination_id] / 1000

        return get_soc_delta(distance * 1.4)
