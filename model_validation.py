import sys
import datetime
import multiprocessing as mp

import numpy as np
import pandas as pd

from Loading.load_data import get_input_data
from Loading.load_data import read_sim_input_data

from DataStructures.City import City

from SingleRun.get_traceB_input import get_traceB_input
from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_traceB_sim import run_traceB_sim
from SingleRun.run_eventG_sim import run_eventG_sim
from SingleRun.run_eventG_sim import get_eventG_sim_stats

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

"""
Init general conf and data structure
"""

from SimulationInput.confs.model_validation_conf import sim_general_conf
from SimulationInput.confs.model_validation_conf import sim_scenario_conf

city = "Torino"
sim_general_conf["city"] = city
sim_general_conf["bin_side_length"] = 500
bookings, grid = read_sim_input_data(city)

city_obj = City\
    (city,
     sim_general_conf)

# simInput_traceB = get_traceB_input\
#     ((sim_general_conf,
#      sim_scenario_conf,
#      city_obj))
#
# sim_traceB = run_traceB_sim\
#     (simInput = simInput_traceB)
#
# simOutput_traceB = EFFCS_SimOutput(sim_traceB)
# #print (simOutput_traceB.sim_stats)
#
# simInput_eventG = get_eventG_input\
#     ((sim_general_conf,
#      sim_scenario_conf,
#      city_obj))
#
# sim_eventG = run_eventG_sim\
#     (simInput = simInput_eventG)
#
# simOutput_eventG = EFFCS_SimOutput(sim_eventG)
# #print (simOutput_eventG.sim_stats)
# sim_stats = simOutput_eventG.sim_stats
#
# #print (simOutput_eventG.sim_stats)
#
# sim_stats_comparison = \
#     pd.concat([simOutput_traceB.sim_stats,
#                simOutput_eventG.sim_stats],
#     axis=1, sort=False)
#
# sim_reqs_eventG = \
#     simOutput_eventG.sim_booking_requests
# sim_reqs_traceB = \
#     simOutput_traceB.sim_booking_requests
#
# print(sim_reqs_eventG.shape[0],
#       sim_reqs_traceB.shape[0])
#
# print(len(sim_reqs_eventG.date.unique()),
#       len(sim_reqs_traceB.date.unique()))
#
# trace_timeouts = \
#     sim_reqs_traceB.ia_timeout.loc\
#     [sim_reqs_traceB.ia_timeout < 5000]
#
# from SingleRun.model_validation_plot import plot_ia_validation
# plot_ia_validation(1000, city, sim_reqs_eventG, trace_timeouts)