import datetime

sim_scenario_conf = {

	"requests_rate_factor": 1,
	"n_cars_factor": 1,
	"time_estimation": True,

	"queuing": True,
	"alpha": 25,
	"beta": 100,

	"hub": False,
	"hub_zone_policy": "num_parkings",
	"n_poles_n_cars_factor": 0.07,

	"distributed_cps": True,
	"cps_placement_policy": "num_parkings",
	"cps_zones_percentage": 0.1,

	"user_contribution": True,
	"system_cps": True,
	"willingness": 0.0,

	"relocation": False,
	"finite_workers": False,

}
