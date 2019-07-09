import datetime

from Simulation.EventG_EFFCS_Sim import EventG_EFFCS_Sim

def run_eventG_sim (simInput):

    print ("Running event generation based simulation ..")
        
    sim_eventG = EventG_EFFCS_Sim(
    
                simInput=simInput
    
            )

    sim_eventG.init_data_structures()    
    t0 = datetime.datetime.now()
    sim_eventG.run()
    t1 = datetime.datetime.now()
    print (t1 - t0)
    
    return sim_eventG
