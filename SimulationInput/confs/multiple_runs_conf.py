import datetime

sim_general_conf = {

    "model_start": datetime.datetime(2017, 10, 1),
    "model_end": datetime.datetime(2017, 11, 1),
    "sim_start": datetime.datetime(2017, 10, 1),
    "sim_end": datetime.datetime(2017, 11, 1)

}

sim_scenario_conf_grid = {

    "requests_rate_factor": [1],
    "n_cars_factor": [1],

    "time_estimation": [True],
    "queuing": [True],
    "alpha": [25],
    "beta": [40, 60, 80, 90],

    "hub": [True],
    "hub_zone_policy": ["num_parkings"],
    "n_poles_n_cars_factor": [0.1],

    "relocation": [True],
    "finite_workers": [False],

    "distributed_cps": [True],
    "cps_placement_policy": ["num_parkings"],
    "n_charging_poles": [20],
    "cps_zones_percentage": [0.1],

    "user_contribution": [True],
    "system_cps": [True],
    "willingness": [0.99],

}
