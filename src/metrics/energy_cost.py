
class EnergyCost:
    price = {
        "LPS": 13.28,
        "MPS": 14.19,
        "HPS": 17.70,
        "CW": 0.354,
        "Refrigerated": 4.354,
        "Electricity": 16.67
    } # $/GJ
    
    def heating(Q: float, quality: str) -> float:
        '''
        Q: Heat duty (GJ/h)
        quality: LPS - MPS - HPS
        return: Cost (k$/year)
        '''
        cost =EnergyCost.price[quality]*Q*8000
        return cost/1e3

    def cooling(Q: float, quality: str) -> float:
        '''
        Q: Heat duty (GJ/h)
        quality: CW - Refrigerated
        return: Cost (k$/year)
        '''
        cost =EnergyCost.price[quality]*Q*8000
        return cost/1e3
    
    def electricity(Q: float) -> float: 
        '''
        Q: Heat duty (GJ/h)
        return: Cost (k$/year)
        '''
        cost =EnergyCost.price["Electricity"]*Q*8000
        return cost/1e3

