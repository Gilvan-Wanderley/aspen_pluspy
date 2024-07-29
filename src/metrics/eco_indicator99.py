

class EcoIndicator99:
    def __init__(self) -> None:
        self._damage_categories = {
            "human": { "normal": 6.49e1, "weight": 400 },
            "ecosystem": { "normal": 1.95e-4, "weight": 400 },
            "resource": { "normal": 1.19e-4, "weight": 200 }
        }

        self._steam = {
            "human": [4.53e-9, 1.02e-10, 6.01e-8, 4.88e-8, 8.10e-11, 3.03e-11],
            "ecosystem": [3.63e-2, 1.55e-3, 1.10e-3],
            "resource": [3.71e-4, 5.25e-1]
        }

        self._elect = {
            "human": [1.68e-8, 6.96e-11, 1.60e-7, 3.17e-8, 4.69e-9, 5.23e-11],
            "ecosystem": [2.14e-3, 3.60e-3, 6.00e-3],
            "resource": [2.40e-4, 5.10e-2]
        }

 
    def steam(self, LCI: float) -> float:
        '''
        LCI: vapor (kg/year)
        return: EI99 (-)
        '''
        EI99 = 0
        for c in self._damage_categories:
            impacts = sum(self._steam[c])
            damage_n = self._damage_categories[c]["normal"]
            damage_w = self._damage_categories[c]["weight"]
            EI99 += LCI*impacts*damage_n*damage_w

        return EI99
    
    def electricity(self, LCI: float) -> float:
        '''
        LCI: electricity (MJ/year)
        return: EI99 (-)
        '''
        EI99 = 0
        for c in self._damage_categories:
            impacts = sum(self._elect[c])
            damage_n = self._damage_categories[c]["normal"]
            damage_w = self._damage_categories[c]["weight"]
            EI99 += LCI*impacts*damage_n*damage_w

        return EI99


if __name__ == "__main__":
    ei99 = EcoIndicator99()
    vapor = ei99.steam(837582)
    elect = ei99.electricity(16832)
    print(f"steam: {vapor}")
    print(f"electricity: {elect}")
