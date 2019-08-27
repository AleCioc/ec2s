import sys

from DataStructures.City import City

from Loading.load_data import read_sim_input_data

from SingleRun.get_eventG_input import get_eventG_input
from SingleRun.run_eventG_sim import run_eventG_sim

from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

from SimulationInput.confs.single_run_conf import sim_general_conf
from SimulationInput.confs.single_run_conf import sim_scenario_conf

city = sys.argv[1]
sim_general_conf["city"] = city
sim_general_conf["bin_side_length"] = 500
bookings, grid = read_sim_input_data(city)

"""
Single Run
"""

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

#fig, ax = plt.subplots(1,1)
#grid.plot(color="white", edgecolor="black", ax=ax)
#grid.loc[simInput_eventG.valid_zones, "valid"] = True
#grid.dropna(subset=["valid"]).plot\
#    (color="lavender", edgecolor="blue", column="valid", ax=ax).plot()
#grid.iloc[200:201].plot(ax=ax)
#grid.iloc[350:351].plot(ax=ax)
#grid.iloc[620:621].plot(ax=ax)
