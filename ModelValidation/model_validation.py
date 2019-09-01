import os

from DataStructures.City import City

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_traceB_sim import run_traceB_sim
from SingleRun.run_eventG_sim import run_eventG_sim

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

from SimulationInput.confs.model_validation_conf import sim_general_conf
from SimulationInput.confs.model_validation_conf import sim_scenario_conf

from ModelValidation.model_validation_plot import plot_ia_validation
from ModelValidation.model_validation_plot import plot_tot_reqs_count
from ModelValidation.model_validation_plot import plot_tot_reqs_count_err
from ModelValidation.model_validation_plot import plot_tot_reqs_count_err_agg
from ModelValidation.model_validation_plot import plot_regr_qq_sns
from ModelValidation.model_validation_plot import plot_od_err
from ModelValidation.model_validation_plot import plot_hourly_daytype_err

def run_model_validation (city):

    results_path = os.path.join(os.getcwd(), "Results", city, "validation")
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    sim_general_conf["city"] = city
    sim_general_conf["bin_side_length"] = 500

    city_obj = City\
        (city,
         sim_general_conf)

    simInput_traceB = get_traceB_input\
        ((sim_general_conf,
         sim_scenario_conf,
         city_obj))
    sim_traceB = run_traceB_sim\
        (simInput = simInput_traceB)
    simOutput_traceB = EFFCS_SimOutput(sim_traceB)

    simInput_eventG = get_eventG_input\
        ((sim_general_conf,
         sim_scenario_conf,
         city_obj))
    sim_eventG = run_eventG_sim\
        (simInput = simInput_eventG)
    simOutput_eventG = EFFCS_SimOutput(sim_eventG)

    sim_reqs_eventG = \
        simOutput_eventG.sim_booking_requests
    sim_reqs_traceB = \
        simOutput_traceB.sim_booking_requests

    trace_timeouts = \
        sim_reqs_traceB.ia_timeout.loc\
        [sim_reqs_traceB.ia_timeout < 5000]

    # plot_ia_validation(1000, city, sim_reqs_eventG, trace_timeouts)
    # plot_tot_reqs_count("hour", True, city, sim_reqs_eventG, sim_reqs_traceB)
    # plot_tot_reqs_count_err("hour", True, city, sim_reqs_eventG, sim_reqs_traceB)
    # plot_tot_reqs_count_err_agg("hour", True, city, sim_reqs_eventG, sim_reqs_traceB)
    # plot_regr_qq_sns(city, sim_reqs_eventG, trace_timeouts)
    # plot_od_err(city, city_obj.grid, sim_reqs_eventG, sim_reqs_traceB)
    # plot_hourly_daytype_err(city, city_obj.grid, sim_reqs_eventG, sim_reqs_traceB)