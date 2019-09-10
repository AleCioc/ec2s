import os

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)


class EFFCS_MultipleRunsPlotter():

    def __init__(self, sim_outputs, city, sim_type):
        self.city = city
        self.figures_path = os.path.join(os.getcwd(), "Figures", self.city, sim_type)
        if not os.path.exists(self.figures_path):
            os.mkdir(self.figures_path)