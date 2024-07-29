class SimulatedAnnealingConfiguration:
    def __init__(self, 
                 temperature: float = 600,
                 energy_level: float = 0.1,
                 cooling_schedule: float = 0.01,
                 steps: int = 400,
                 mininum_temperature: float = 1e-6) -> None:
        self._temp = temperature
        self._energy = energy_level
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
    def energy_level(self):
        return self._energy