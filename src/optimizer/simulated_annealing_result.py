import numpy as np
from .simulated_annealing_design_variable import SimulatedAnnealingDesignVariable


class SimulatedAnnealingResult:
    def __init__(self,
                 design_variable: SimulatedAnnealingDesignVariable,
                 function_value: float,
                 iterations: int
                 ) -> None:
        self._design_var = design_variable
        self._fotm = function_value
        self._iter = iterations

    @property
    def optimal_real_values(self) -> np.ndarray:
        return self._design_var.real_values
    
    @property
    def optimal_integer_values(self) -> np.ndarray:
        return self._design_var.integer_values
    
    @property
    def real_bounds(self) -> np.ndarray:
        return self._design_var.real_bounds
    
    @property
    def integer_bounds(self) -> np.ndarray:
        return self._design_var.integer_bounds
    
    @property
    def function_value(self) -> float:
        return self._fotm
    
    @property
    def iterations(self) -> int:
        return self._iter