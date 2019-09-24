import datetime

sim_general_conf = {

    "model_start": datetime.datetime(2017, 10, 1),
    "model_end": datetime.datetime(2017, 11, 1),
    "sim_start": datetime.datetime(2017, 10, 1),
    "sim_end": datetime.datetime(2017, 11, 1)

}

sim_scenario_conf = {

    "requests_rate_factor": 1,
    "n_cars_factor": 1.5,

    "time_estimation": True,
    "queuing": True,
    "alpha": 25,
    "beta": 60,

    "hub": True,
    "hub_zone_policy": "num_parkings",
    "n_poles_n_cars_factor": 0.1,

    "relocation": False,
    "finite_workers": False,

    "distributed_cps": True,
    "cps_placement_policy": "num_parkings",
    "cps_zones_percentage": 0.1,

    "user_contribution": True,
    "system_cps": False,
    "willingness": 0.33,

}
