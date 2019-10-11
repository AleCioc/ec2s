import datetime
import numpy as np

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": np.arange(0.5, 1.6, 0.2),

    "time_estimation": [True],
    "queuing": [True],
    "alpha": [25],
    "beta": np.arange(60, 105, 10),

    "hub": [True],
    "hub_zone_policy": ["num_parkings"],
    "n_poles_n_cars_factor" : np.arange(0.05, 0.2, 0.005),

    "relocation": [False],
    "finite_workers": [False],

    "distributed_cps": [False],
    "cps_placement_policy": ["num_parkings"],
    "n_charging_poles": [20],
    "cps_zones_percentage": [0.1],

    "user_contribution": [False],
    "system_cps": [False],
    "willingness": [0.0],

}
