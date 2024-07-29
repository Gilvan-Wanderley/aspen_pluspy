import numpy as np

class SimulatedAnnealingDesignVariable:
    def __init__(self, 
                 real_values: np.ndarray|None,
                 real_bounds: np.ndarray|None,
                 integer_values: np.ndarray|None,
                 integer_bounds: np.ndarray|None,
                 initial_range: float = 0.5) -> None:
        self._x0 = real_values.copy() if real_values is not None else None
        self._y0 = integer_values.copy() if integer_values is not None else None
        self._bndsx = real_bounds.copy() if real_bounds is not None else None
        self._bndsy = integer_bounds.copy() if integer_bounds is not None else None
        self._range = initial_range

    @property
    def real_values(self) -> np.ndarray:
        return self._x0
    
    @property
    def integer_values(self) -> np.ndarray:
        return self._y0
    
    @property
    def real_bounds(self) -> np.ndarray:
        return self._bndsx
    
    @property
    def integer_bounds(self) -> np.ndarray:
        return self._bndsy

    
    def generate_real(self, x0: np.ndarray|None, ratio: float) -> np.ndarray|None:
        if x0 is None:
            return None
        x = np.zeros(len(x0))
        for i in range(len(x0)):
            u = np.random.rand()
            if ratio == 1:
                x[i] = self._bndsx[i][0] + u*(self._bndsx[i][1] - self._bndsx[i][0])
            else:
                f = ratio*self._range
                lb = x0[i]*(1-f) if x0[i]*(1-f) > self._bndsx[i][0] else self._bndsx[i][0]
                ub = x0[i]*(1+f) if x0[i]*(1+f) < self._bndsx[i][1] else self._bndsx[i][1]
                x[i] = lb + u*(ub - lb)    
        return x
    
    def generate_integer(self, y0: np.ndarray|None, ratio: float) -> np.ndarray|None:
        if y0 is None:
            return None
        y = np.zeros(len(y0))
        for i in range(len(y0)):
            if ratio == 1:
                y[i] = np.random.randint(self._bndsy[i][0], self._bndsy[i][1] + 1)
            else:
                f = ratio*self._range
                lb = y0[i]*(1-f) if y0[i]*(1-f) > self._bndsy[i][0] else self._bndsy[i][0]
                ub = y0[i]*(1+f) if y0[i]*(1+f) < self._bndsy[i][1] else self._bndsy[i][1]
                y[i] = np.random.randint(np.trunc(lb), np.trunc(ub) + 1) 
        return y
