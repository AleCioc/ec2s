import datetime

from SimulationInput.EFFCS_SimInput import EFFCS_SimInput

def get_traceB_input (sim_general_conf,
                      sim_scenario_conf, 
                      grid, 
                      bookings):

    print ("Creating traceB simulation input ..")
    t0 = datetime.datetime.now()
    simInput = EFFCS_SimInput\
         (sim_general_conf,
          sim_scenario_conf,
          grid=grid,
          bookings=bookings)
    simInput.get_input_bookings_filtered()
    simInput.get_neighbors_dicts()
    simInput.get_booking_requests_list()
    simInput.get_valid_zones()
    simInput.init_cars()
    simInput.init_cars_dicts()
    simInput.init_charging_poles()
    t1 = datetime.datetime.now()
    print (t1 - t0)

    return simInput
