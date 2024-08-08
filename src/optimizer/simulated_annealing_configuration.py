class SimulatedAnnealingConfiguration:
    def __init__(self, 
                 temperature: float = 600,
                 normal_factor: float = 10.0,
                 cooling_schedule: float = 0.01,
                 steps: int = 400,
                 mininum_temperature: float = 1e-6) -> None:
        self._temp = temperature
        self._normal = normal_factor
        self._cooling = cooling_schedule
        self._steps = steps
        self._tmin = mininum_temperature

    @property
    def temperature(self):
        return self._temp
    
    @property
    def cooling_schedule(self):
        return self._cooling
    
    @property
    def steps(self):
        return self._steps
    
    @property
    def mininum_temperature(self):
        return self._tmin
    
    @property
    def normal_factor(self):
        return self._normal