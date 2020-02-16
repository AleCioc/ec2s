import itertools
import datetime
import numpy as np

class EFFCS_SimConfGrid ():
    
    def __init__ (self, general_conf, conf_grid):

        self.conf_keys = conf_grid.values()
        self.conf_list = []        
        for el in itertools.product(*conf_grid.values()):
#            print (el)
            conf = {k:None for k in conf_grid}
            i = 0
            for k in conf.keys():
                conf[k] = el[i]
                i += 1
            self.conf_list += [conf]
        print(len(self.conf_list))
        print(len(list(set(self.conf_list))))

