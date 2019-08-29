import datetime
import numpy as np

sim_general_conf = {

    "model_start": datetime.datetime(2017, 9, 1),
    "model_end": datetime.datetime(2017, 10, 1),
    "sim_start": datetime.datetime(2017, 10, 1),
    "sim_end": datetime.datetime(2017, 11, 1)

}

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],

    "time_estimation": [False],
    "queuing": [True, False],
    "alpha": [25],
    "beta": [60, 80, 100],

    "hub": [True],
    "hub_zone_policy": ["num_parkings"],
    "hub_zone" : []
    "hub_n_charging_poles": np.arange(20, 80, 5),

    "relocation": [True],
    "finite_workers": [False],

    "distributed_cps": [False],
    "cps_placement_policy": ["manual"],
    "n_charging_poles": [20],
    "cps_zones_percentage": [0.1],

    "user_contribution": [False],
    "system_cps": [False],
    "willingness": [0.99],

}
