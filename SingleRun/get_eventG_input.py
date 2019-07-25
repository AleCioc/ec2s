import datetime

from SimulationInput.EFFCS_SimInput import EFFCS_SimInput

def get_eventG_input (conf_tuple):

    print ("Creating eventG simulation input ..")
    t0 = datetime.datetime.now()
    simInput = EFFCS_SimInput\
         (conf_tuple)
    simInput.get_input_bookings_filtered()
    simInput.get_neighbors_dicts()
    simInput.get_requests_rates()
    simInput.get_trip_kdes()
    simInput.get_valid_zones()
    simInput.init_cars()
    simInput.init_cars_dicts()
    simInput.init_charging_poles()
    t1 = datetime.datetime.now()
    print (t1 - t0)

    return simInput