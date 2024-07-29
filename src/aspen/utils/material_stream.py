from aspen.aspen_simulation import AspenSimulation

class MaterialStream:
    def __init__(self, stream_name: str, simulation: AspenSimulation) -> None:
        self._name = stream_name
        self._sim = simulation

    @property
    def temperature(self) -> float: 
        path = f"\\Data\\Streams\\{self._name}\\Output\\TEMP_OUT\\MIXED"
        value = self._sim.get_variable_by_path(path)
        return value
    
    @property
    def mole_frac(self, component: str) -> float: 
        path = f"\\Data\\Streams\\{self._name}\\Output\\MOLEFRAC\\MIXED\\{component}"
        value = self._sim.get_variable_by_path(path)
        return value