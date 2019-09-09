import os

import pandas as pd

from DataStructures.City import City

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import run_eventG_sim

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput
from SimulationOutput.EFFCS_SimOutputPlotter import EFFCS_SimOutputPlotter

def single_run(city, sim_type, sim_general_conf, sim_scenario_conf):

    results_path = os.path.join(os.getcwd(), "Results", city, sim_type)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    sim_general_conf["city"] = city
    sim_general_conf["bin_side_length"] = 500

    city_obj = City\
        (city,
         sim_general_conf)

    simInput_eventG = get_eventG_input\
        ((sim_general_conf,
         sim_scenario_conf,
         city_obj))
    sim_eventG = run_eventG_sim\
        (simInput = simInput_eventG)
    simOutput_eventG = EFFCS_SimOutput(sim_eventG)
    sim_stats  = simOutput_eventG.sim_stats

    sim_stats.to_pickle\
        (os.path.join(results_path,
                      sim_type + ".pickle"))

    pd.Series(sim_general_conf).to_pickle\
        (os.path.join(results_path,
                      "sim_general_conf.pickle"))

    pd.Series(sim_scenario_conf).to_pickle\
        (os.path.join(results_path,
                      "sim_scenario_conf.pickle"))

    plotter = EFFCS_SimOutputPlotter(simOutput_eventG, city, simInput_eventG.grid)
    plotter.plot_events_profile()
    plotter.plot_charging_duration_hist()
    plotter.plot_n_charges_avg()
    plotter.plot_charging_energy_avg()
    plotter.plot_n_charges_t()
    plotter.plot_tot_energy()
    plotter.plot_fleet_status()
    plotter.plot_n_cars_charging()
    plotter.plot_charging_t_hist()
    plotter.plot_origin_heatmap()
    plotter.plot_charging_heatmap_system()
    plotter.plot_charging_heatmap_users()
    plotter.plot_unsatisfied_t_hist()
    plotter.plot_unsatisfied_origins_heatmap()
    plotter.plot_deaths_t_hist()
    plotter.plot_deaths_origins_heatmap()
    plotter.plot_charge_deaths_t_hist()
    plotter.plot_charge_deaths_origins_heatmap()
    plotter.plot_relo_cost_t()
