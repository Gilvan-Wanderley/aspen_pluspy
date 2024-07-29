from aspen.aspen_simulation import AspenSimulation
from aspen.utils.aspen_variable import AspenVariable
from optimizer.simulated_annealing import SimulatedAnnealing
from optimizer.simulated_annealing_configuration import SimulatedAnnealingConfiguration
from optimizer.simulated_annealing_design_variable import SimulatedAnnealingDesignVariable
from datetime import datetime
import pandas as pd
import numpy as np


def setup(x, y): 
    global count_
    global simulation

    if count_ >= 500:        
            del simulation
            simulation = AspenSimulation(simulation_file, variables)
            count_ = 0

    # begin: setup the simulation

    # end

    simulation.run()
    count_ = count_  + 1

def func(x, y):
    setup(x, y)

    # begin: constrains and objective function 


    fval = 0.0
    # end

    return fval

variables = [ ]
tracking = []


count_ = 0
simulation_file = "ACN-H2O_Conventional_S1.bkp"
historian = pd.DataFrame(columns=tracking, index=pd.Index([], name="id"))

try:
    simulation = AspenSimulation(simulation_file, variables)

    x0 = np.array([101300])
    y0 = np.array([20, 8])
      
    bndsx = np.array([[81060, 202650]])
    bndsy = np.array([[16, 25], [6, 12]])

    design_var = SimulatedAnnealingDesignVariable(x0, bndsx, y0, bndsy)

    conf = SimulatedAnnealingConfiguration(steps=100, 
                                           cooling_schedule=0.1)

    optimizer = SimulatedAnnealing(conf)

    result = optimizer.solver(func, design_var)
    
finally:
    historian.to_csv(f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}-{simulation_file[:-4]}.csv")
    del simulation
      