from aspen.aspen_simulation import AspenSimulation


class RadFracBlock:
    def __init__(self, block_name: str, simulation: AspenSimulation) -> None:
        self._name = block_name
        self._sim = simulation

    @property
    def num_stage(self) -> int:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\NSTAGE"
        value = self._sim.get_variable_by_path(path)
        return value
    
    @num_stage.setter
    def num_stage(self, value: int) -> None:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\NSTAGE"
        self._sim.set_variable_by_path(path, value)

    def get_feed_stage(self, stream_name: str) -> int:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\FEED_STAGE\\{stream_name}"
        value = self._sim.get_variable_by_path(path)
        return value
    
    def set_feed_stage(self, stream_name: str, value: int) -> None:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\FEED_STAGE\\{stream_name}"
        self._sim.set_variable_by_path(path, value)

    @property
    def pressure(self) -> float:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\PRES1"
        value = self._sim.get_variable_by_path(path)
        return value
    
    @pressure.setter
    def pressure(self, value: float) -> None:
        path = f"\\Data\\Blocks\\{self._name}\\Input\\PRES1"
        self._sim.set_variable_by_path(path, value)

    def temperature_stage(self, number_stage: int) -> float:
        path = f"\\Data\\Blocks\\{self._name}\\Output\\B_TEMP\\{number_stage}"
        value = self._sim.get_variable_by_path(path)
        return value
    
    def reboiler_duty(self) -> float:
        path = f"\\Data\\Blocks\\{self._name}\\Output\\REB_DUTY"
        value = self._sim.get_variable_by_path(path)
        return value
    
    def condenser_duty(self) -> float:
        path = f"\\Data\\Blocks\\{self._name}\\Output\\COND_DUTY"
        value = self._sim.get_variable_by_path(path)
        return value