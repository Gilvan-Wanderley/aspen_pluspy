
class EnergyCost:
    price = {
        "LPS": 13.28,
        "MPS": 14.19,
        "HPS": 17.70,
        "CW": 0.354,
        "Refrigerated": 4.354,
        "Electricity": 16.67
    } # $/GJ
    
    heat = {
        "LPS": 2081.4,
        "MPS": 1999.0,
        "HPS": 1639.9,
        "CW": 41.7274985,
    } # kJ/kg

    enthalpy = {
        "LPS": 2360,
        "MPS": 2396,
        "HPS": 2476
    } # kJ/kg

    fuel = {
        "Oil" : {
            "NHV": 39771,
            "C%": 86.5
        },
        "NG": {
            "NHV": 51600,
            "C%": 75.4
        }
    }

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


    def co2_emission_fuel(Q: float, quality: str, fuel: str) -> float:
        '''
        Q: Heat duty (kJ/h)
        quality: LPS - MPS - HPS
        comb: Oil, NG
        return: CO2 Emission (kg/h)
        '''
        Tamb= 298
        Tstack = 433
        Tftb = 2073
        alfa = 3.67

        NHV = EnergyCost.fuel[fuel]["NHV"]
        C_ = EnergyCost.fuel[fuel]["C%"]
        dh = EnergyCost.enthalpy[quality]
        k = EnergyCost.heat[quality]
        
        co2 = (Q/NHV)*(C_/100)*(dh/k)*((Tftb - Tamb)/(Tftb - Tstack))*alfa

        return co2
    
    def  co2_emission_elec(E: float) -> float:
        '''
        E: Electricity (GJ/h)
        return: CO2 Emission (kg/h)
        '''
        factor = 51.1 # kg/GJ
        return factor*E