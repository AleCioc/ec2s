import datetime
import numpy as np

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],

    "time_estimation": [True],
    "queuing": [True],
    "alpha": np.arange(5, 105, 5),
    "beta": [100],

    "hub": [False],
    "hub_zone_policy": ["num_parkings"],
    "n_poles_n_cars_factor": [0.1],

    "relocation": [False],
    "finite_workers": [False],

    "distributed_cps": [True],
    "cps_placement_policy": ["num_parkings"],
    "cps_zones_percentage": [0.1],

    "system_cps": [True],
    "user_contribution": [True],
    "willingness": [0, 0.33, 0.66, 0.99],

}
