from aspen.aspen_simulation import AspenSimulation
from aspen.utils.aspen_variable import AspenVariable
from optimizer.simulated_annealing import SimulatedAnnealing
from optimizer.simulated_annealing_configuration import SimulatedAnnealingConfiguration
from optimizer.simulated_annealing_design_variable import SimulatedAnnealingDesignVariable
from datetime import datetime
import pandas as pd
import numpy as np
from metrics.energy_cost import EnergyCost as ec
from metrics.equipments_cost import EquipmentsCost as eq
from metrics.eco_indicator99 import EcoIndicator99
def setup(x, y): 
    global count_
    global simulation

    if count_ >= 500:        
            del simulation
            simulation = AspenSimulation(simulation_file, variables)
            count_ = 0

    # begin: setup the simulation

    # end

    simulation.run()
    count_ = count_  + 1

def func(x, y):
    setup(x, y)

    # begin: constrains and objective function 

    B2_ACN = simulation.get_variable("B2_ACN")
    if B2_ACN < 0.999899 :
         return np.inf

    time = 8000.0 # h/year

    Qc_LPC = -simulation.get_variable("QC_LPC") # kW
    # Mcw_LPC = Qc_LPC/ec.heat["CW"]*3600 # kg/h
    Ccw_LPC = Qc_LPC*ec.price["CW"]*time*3.6/(1e3) # $/year

    Qr_LPC = simulation.get_variable("QR_LPC") # kW
    Ms_LPC = Qr_LPC/ec.heat["LPS"]*3600 # kg/h
    Cs_LPC = Qr_LPC*ec.price["LPS"]*time*3.6/(1e3) # $/year


    Qc_HPC = -simulation.get_variable("QC_HPC") # kW
    # Mcw_HPC = Qc_HPC/ec.heat["CW"]*3600 # kg/h
    Ccw_HPC = Qc_HPC*ec.price["CW"]*time*3.6/(1e3) # $/year
    
    Qr_HPC = simulation.get_variable("QR_HPC") # kW
    Ms_HPC = Qr_HPC/ec.heat["LPS"]*3600 # kg/h
    Cs_HPC = Qr_HPC*ec.price["LPS"]*time*3.6/(1e3) # $/year
    

    p1_elec = simulation.get_variable("P1_ELEC") # kW
    Qp1_elec = p1_elec*3.6 # MJ/h
    Cp1_elec = p1_elec*ec.price["Electricity"]*time*3.6/(1e6) # K$/year


    MaS = 1431.7
    playback = 3
    NT_LPC = simulation.get_variable("NT_LPC") # -
    d_LPC = simulation.get_variable("d_LPC") # m
    P_LPC = simulation.get_variable("P_LPC")*0.986923 # atm
    Tc_cin_LPC = 273.15 + 25 # K
    Tc_cout_LPC = 273.15 + 35 # K
    Tc_hin_LPC = simulation.get_variable_by_path("\\Data\\Blocks\\LPC\\Output\\B_TEMP\\2") # K
    Tc_hout_LPC = simulation.get_variable_by_path("\\Data\\Blocks\\LPC\\Output\\B_TEMP\\1") # K
    Tr_cin_LPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\LPC\\Output\\B_TEMP\\{NT_LPC-1}") # K
    Tr_cout_LPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\LPC\\Output\\B_TEMP\\{NT_LPC}") # K
    Tr_hin_LPC = 433 # K
    Tr_hout_LPC = 432 # K
    
    Cvessel_LPC = eq.column_vessel(MaS, d_LPC, NT_LPC, P_LPC) # k$
    Ctray_LPC = eq.column_plate(MaS, d_LPC, NT_LPC) # k$
    Ccond_LPC = eq.heat_exchanger(MaS, Qc_LPC, Tc_hin_LPC, Tc_hout_LPC, Tc_cin_LPC, Tc_cout_LPC, P_LPC, False) # kR$
    Creb_LPC = eq.heat_exchanger(MaS, Qr_LPC, Tr_hin_LPC, Tr_hout_LPC, Tr_cin_LPC, Tr_cout_LPC, P_LPC, True) # kR$

    CLPC = Cvessel_LPC + Ctray_LPC + Ccond_LPC + Creb_LPC # k$

    NT_HPC = simulation.get_variable("NT_HPC") # - 
    d_HPC = simulation.get_variable("d_HPC") # m
    P_HPC = simulation.get_variable("P_HPC")*0.986923 # atm
    Tc_cin_HPC = 273.15 + 25 # K
    Tc_cout_HPC = 273.15 + 35 # K
    Tc_hin_HPC = simulation.get_variable_by_path("\\Data\\Blocks\\HPC\\Output\\B_TEMP\\2") # K
    Tc_hout_HPC = simulation.get_variable_by_path("\\Data\\Blocks\\HPC\\Output\\B_TEMP\\1") # K
    Tr_cin_HPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\HPC\\Output\\B_TEMP\\{NT_HPC-1}") # K
    Tr_cout_HPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\HPC\\Output\\B_TEMP\\{NT_HPC}") # K
    Tr_hin_HPC = 433 # K
    Tr_hout_HPC = 432 # K

    Cvessel_HPC = eq.column_vessel(MaS, d_HPC, NT_HPC, P_HPC) # k$
    Ctray_HPC = eq.column_plate(MaS, d_HPC, NT_HPC) # k$
    Ccond_HPC = eq.heat_exchanger(MaS, Qc_HPC, Tc_hin_HPC, Tc_hout_HPC, Tc_cin_HPC, Tc_cout_HPC, P_HPC, False) # kR$
    Creb_HPC = eq.heat_exchanger(MaS, Qr_HPC, Tr_hin_HPC, Tr_hout_HPC, Tr_cin_HPC, Tr_cout_HPC, P_HPC, True) # kR$

    CHPC = Cvessel_HPC + Ctray_HPC + Ccond_HPC + Creb_HPC # k$
    
    Copex_LPC = (Ccw_LPC + Cs_LPC)/(1e3) # K$/year
    Copex_HPC = (Ccw_HPC + Cs_HPC)/(1e3) # K$/year
    TOC = Copex_LPC + Copex_HPC + Cp1_elec # k$/year

    TCC = CLPC + CHPC # k$
    TAC = TCC/playback + TOC # k$/year

    ei99_calc = EcoIndicator99()
    ei99_steam = ei99_calc.steam((Ms_LPC + Ms_HPC)*time)
    ei99_elect = ei99_calc.electricity(Qp1_elec*time)
    EI99 = ei99_steam + ei99_elect
    # end

    NF_F1 = simulation.get_variable("NF_F1")
    NF_D1 = simulation.get_variable("NF_D1")
    NF_D2 = simulation.get_variable("NF_D2")
    P_LPC = P_LPC/0.986923
    P_HPC = P_HPC/0.986923
    RR_LPC = simulation.get_variable("RR_LPC")
    RR_HPC = simulation.get_variable("RR_HPC")
    CO2_Oil = ec.co2_emission_fuel((Qr_LPC + Qr_HPC)*3600, "LPS", "Oil")
    CO2_NG = ec.co2_emission_fuel((Qr_LPC + Qr_HPC)*3600, "LPS", "NG")
    CO2_Ele = ec.co2_emission_elec(Qp1_elec/1e9)
    tracking = [NT_LPC, NT_HPC, NF_F1, NF_D1, NF_D2, P_LPC, P_HPC, RR_LPC, RR_HPC,
                TAC, TCC, TOC, EI99, CO2_Oil, CO2_NG, CO2_Ele,
                B2_ACN, ]
    save(tracking)  

    return TAC

def save(tracking):
    data ={}
    for i, var in enumerate(tracking):
         data[tags[i]] = var

    historian.loc[len(historian)] = data

tags = ["NT-LPC", "NT-HPC", "NF-F1", "NF-D1", "NF-D2", "P-LPC(bar)", "P-HPC(bar)", "RR_LPC", "RR_HPC",
        "TAC(k$/year)", "TCC(k$)", "TOC(k$/year)", "EI99", "CO2_Oil(kg/h)", "CO2_NG(kg/h)", "CO2_Elec(kg/h)",
        "B2_ACN", ]
count_ = 0
simulation_file = "ACN-H2O_Conventional_S1.bkp"
historian = pd.DataFrame(columns=tags, index=pd.Index([], name="id"))
variables = [ 
    AspenVariable("NT_LPC", "\\Data\\Blocks\\LPC\\Input\\NSTAGE"),
    AspenVariable("NT_HPC", "\\Data\\Blocks\\HPC\\Input\\NSTAGE"),
    AspenVariable("NT_LPC_CI", "\\Data\\Blocks\\LPC\\Subobjects\\Column Internals\\INT-1\\Subobjects\\Sections\\CS-1\\Input\\CA_STAGE2\\INT-1\\CS-1"),
    AspenVariable("NT_HPC_CI", "\\Data\\Blocks\\HPC\\Subobjects\\Column Internals\\INT-1\\Subobjects\\Sections\\CS-1\\Input\\CA_STAGE2\\INT-1\\CS-1"),
    AspenVariable("d_LPC","\\Data\\Blocks\\LPC\\Subobjects\\Column Internals\\INT-1\\Output\\CA_DIAM6\\INT-1\\CS-1"),
    AspenVariable("d_HPC","\\Data\\Blocks\\HPC\\Subobjects\\Column Internals\\INT-1\\Output\\CA_DIAM6\\INT-1\\CS-1"),
    AspenVariable("P_LPC", "\\Data\\Blocks\\LPC\\Input\\PRES1"),
    AspenVariable("P_HPC", "\\Data\\Blocks\\HPC\\Input\\PRES1"),
    AspenVariable("P_F1", "\\Data\\Streams\\F1\\Input\\PRES\\MIXED"),
    AspenVariable("P_P1", "\\Data\\Blocks\\P1\\Input\\PRES"),
    AspenVariable("NF_F1", "\\Data\\Blocks\\LPC\\Input\\FEED_STAGE\\F1"),
    AspenVariable("NF_D1", "\\Data\\Blocks\\HPC\\Input\\FEED_STAGE\\F2"),
    AspenVariable("NF_D2", "\\Data\\Blocks\\LPC\\Input\\FEED_STAGE\\D2"),
    AspenVariable("RR_LPC", "\\Data\\Blocks\\LPC\\Input\\BASIS_RR"),
    AspenVariable("RR_HPC", "\\Data\\Blocks\\HPC\\Input\\BASIS_RR"),
    AspenVariable("QC_LPC", "\\Data\\Blocks\\LPC\\Output\\COND_DUTY"),
    AspenVariable("QC_HPC", "\\Data\\Blocks\\HPC\\Output\\COND_DUTY"),
    AspenVariable("QR_LPC", "\\Data\\Blocks\\LPC\\Output\\REB_DUTY"),
    AspenVariable("QR_HPC", "\\Data\\Blocks\\HPC\\Output\\REB_DUTY"),
    AspenVariable("P1_ELEC", "\\Data\\Blocks\\P1\\Output\\ELEC_POWER"),
    AspenVariable("B2_ACN","\\Data\\Streams\\B2\\Output\\MOLEFRAC\\MIXED\\ACN")
]

try:
    simulation = AspenSimulation(simulation_file, variables)

    # x0 = np.array([101300])
    # y0 = np.array([20, 8])
      
    # bndsx = np.array([[81060, 202650]])
    # bndsy = np.array([[16, 25], [6, 12]])

    # design_var = SimulatedAnnealingDesignVariable(x0, bndsx, y0, bndsy)

    # conf = SimulatedAnnealingConfiguration(steps=100, 
    #                                        cooling_schedule=0.1)

    # optimizer = SimulatedAnnealing(conf)

    # result = optimizer.solver(func, design_var)
    
finally:
    historian.to_csv(f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}-{simulation_file[:-4]}.csv")
    del simulation
      