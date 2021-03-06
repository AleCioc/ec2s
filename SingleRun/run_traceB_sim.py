import datetime

from Simulation.TraceB_EFFCS_Sim import TraceB_EFFCS_Sim
from SimulationOutput.EFFCS_SimOutput import EFFCS_SimOutput

def run_traceB_sim (simInput):

    # print ("Running trace based simulation ..")
        
    sim_traceB = TraceB_EFFCS_Sim(
    
                simInput=simInput,
    
            )
    
    # t0 = datetime.datetime.now()
    sim_traceB.run()
    # t1 = datetime.datetime.now()
    # print (t1 - t0)
    
    return sim_traceB


def get_traceB_sim_stats(simInput):
    sim_traceB = run_traceB_sim(simInput)
    simOutput_traceB = EFFCS_SimOutput(sim_traceB)
    return simOutput_traceB.sim_stats
