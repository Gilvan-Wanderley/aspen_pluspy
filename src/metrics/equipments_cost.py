import math

class EquipmentsCost:
    def column_vessel(index, d, NT, P) -> float:
        '''
        index: M&S 
        d: Diameter (m)
        NT: Number of tray (-)
        P: Pressure (atm)
        return: Cost (k$)
        '''
        Fm = 3.67
        Fp = None

        if P <= 3.4:
            Fp = 1
        elif  P > 3.4 and P <= 6.8:
            Fp = 1.0 + (P - 3.4)*(1.05 - 1.0)/(6.8 - 3.4)
        elif  P > 6.8 and P <= 13.6:
            Fp = 1.05 + (P - 6.8)*(1.15 - 1.05)/(13.6 - 6.8)
        else:
            Fp = 1.15
        
        L = 0.61*(NT/0.75 + 3) + 6
        Fc = Fm*Fp

        cost = (index/280.0)*937.636*(d**1.066)*(L**0.802)*(2.18+Fc)
        return cost/1e3
    
    def column_plate(index, d, NT) -> float:
        '''
        index: M&S 
        d: Diameter (m)
        NT: Number of tray (-)
        return: Cost (k$)
        '''
        Fs = 1.0
        Ft = 0.0
        Fm = 1.70
        
        L = 0.61*(NT/0.75 + 3) + 6
        Fc = Fs + Ft + Fm

        cost = (index/280.0)*97.243*(d**1.55)*L*Fc
        return cost/1e3
    
    def heat_exchanger(index, Q, Thin, Thout, Tcin, Tcout, P, isReb = False ) -> float:
        '''
        index: M&S 
        Q: Heat duty (kW)
        Thin: Inlet temperature hot stream (K)
        Thin: Inlet temperature hot stream (K)
        Thin: Inlet temperature hot stream (K)
        Thin: Inlet temperature hot stream (K)
        P: Pressure (atm)
        isReb: Reboiler flag (bool)
        return: Cost (k$)
        '''
        Fm = 3.75

        Fd = None
        U = None # kW/(m²K)
        if isReb:
            U = 0.568
            Fd = 1.35
        else:
            U=0.852
            Fd = 0.8

        Fp = None

        if P <= 10.2:
            Fp = 0
        elif  P > 10.2 and P <= 20.4:
            Fp = 0.0 + (P - 10.2)*(0.01 - 0.0)/(20.4 - 10.2)
        elif  P > 20.4 and P <= 27.2:
            Fp = 0.01 + (P - 20.4)*(0.25 - 0.01)/(27.2 - 20.4)
        elif  P > 27.2 and P <= 54.4:
            Fp = 0.25 + (P - 27.2)*(0.52 - 0.25)/(54.4 - 27.2)
        else:
            Fp = 0.52
        
        Fc = Fm*(Fp + Fd)
        lmtd = ((Thin - Tcout) - (Thout - Tcin))/(math.log((Thin - Tcout)/(Thout - Tcin)))
        A = Q/(U*lmtd)

        cost = (index/280.0)*474.668*(A**0.65)*(2.29 + Fc)
        return cost/1e3

