class AspenVariable:
    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def path(self) -> str:
        return self._path