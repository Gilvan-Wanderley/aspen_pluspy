import numpy as np
from typing import Callable
from .simulated_annealing_configuration import SimulatedAnnealingConfiguration
from .simulated_annealing_design_variable import SimulatedAnnealingDesignVariable
from .simulated_annealing_result import SimulatedAnnealingResult


class SimulatedAnnealing:
    def __init__(self, configuration: SimulatedAnnealingConfiguration) -> None:
        self._conf = configuration
        self._temp = None
        self._func = None
    
    def _object_func(self, x: np.ndarray, y: np.ndarray):
        try:
            return self._func(x, y)
        except:
            return np.inf

    def solver(self, 
               object_func: Callable[[np.ndarray, np.ndarray], float],
               design_variable: SimulatedAnnealingDesignVariable) -> SimulatedAnnealingResult: 
        self._func = object_func
        criteria = True
        self._temp = self._conf.temperature

        x1 = design_variable.real_values
        y1 = design_variable.integer_values
        f1 = self._object_func(x1, y1)

        [xotm, yotm, fotm] = [x1, y1, f1]

        iterations = 0
        while(criteria):
            i = 0
            while(i < self._conf.steps):
                ratio = self._temp/self._conf.temperature
                x2 = design_variable.generate_real(x1, ratio)
                y2 = design_variable.generate_integer(y1, ratio)
                f2 = self._object_func(x2, y2)

                if f2 - f1 < 0.0:
                    [x1, y1, f1] = [x2, y2, f2]
                    if f2 < fotm:
                        [xotm, yotm, fotm] = [x2, y2, f2]
                else:
                    if np.random.rand() < np.exp(-self._conf.energy_level/self._temp):
                        [x1, y1, f1] = [x2, y2, f2]
                i += 1
                iterations += 1
                print(f"Function: {f1}\nContinuous: {x1}\nDiscrete: {y1}")
                print(f"Temperature: {self._temp}\nIterations: {iterations}")
                print()
            [x1, y1, f1] = [xotm, yotm, fotm]
            self._temp = (1 - self._conf.cooling_schedule)*self._temp
            if self._temp < self._conf.mininum_temperature:
                criteria = False
        
        opt_design_var = SimulatedAnnealingDesignVariable(xotm, design_variable.real_bounds,
                                                          yotm, design_variable.integer_bounds)
        return SimulatedAnnealingResult(opt_design_var, fotm, iterations)