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
    else:
          simulation.reinit()

    # begin: setup the simulation
    RR_LPC = x[0]
    RR_HPC = x[1]
    P_LPC = x[2]
    P_HPC = x[3]

    NT_LPC = y[0]
    NT_HPC = y[1]
    NF_F1 = y[2]
    NF_D1 = y[3]
    NF_D2 = y[4]
    
    simulation.set_variable("RR_LPC", RR_LPC)
    simulation.set_variable("RR_HPC", RR_HPC)
    simulation.set_variable("P_LPC", P_LPC)
    simulation.set_variable("P_HPC", P_HPC)
    simulation.set_variable("P_P1", P_HPC)

    simulation.set_variable("NT_LPC", NT_LPC)
    simulation.set_variable("NT_HPC", NT_HPC)
    simulation.set_variable("NT_LPC_CI", NT_LPC - 1)
    simulation.set_variable("NT_HPC_CI", NT_HPC - 1)
    simulation.set_variable("NF_F1", NF_F1)
    simulation.set_variable("NF_D1", NF_D1)
    simulation.set_variable("NF_D1", NF_D2)

    # end

    simulation.run()
    count_ = count_  + 1

def func(x, y):
    setup(x, y)

    # constrains
    if not simulation.status:
         return np.inf
    
    B2_ACN = simulation.get_variable("B2_ACN")
    if B2_ACN < 0.999899 :
         return np.inf
    
    # end contrains

    time = 8000.0   # h/year
    MaS = 1431.7    # - 

    Qc_LPC = -simulation.get_variable("QC_LPC")     # kW
    Qr_LPC = simulation.get_variable("QR_LPC")      # kW
    Ms_LPC = Qr_LPC/ec.heat["LPS"]*3600             # kg/h
    Cs_LPC = Qr_LPC*ec.price["LPS"]*time*3.6/(1e3)  # $/year
    Ccw_LPC = Qc_LPC*ec.price["CW"]*time*3.6/(1e3)  # $/year

    Qc_HPC = -simulation.get_variable("QC_HPC")     # kW
    Qr_HPC = simulation.get_variable("QR_HPC")      # kW
    Ms_HPC = Qr_HPC/ec.heat["LPS"]*3600             # kg/h
    Ccw_HPC = Qc_HPC*ec.price["CW"]*time*3.6/(1e3)  # $/year
    Cs_HPC = Qr_HPC*ec.price["LPS"]*time*3.6/(1e3)  # $/year

    p1_elec = simulation.get_variable("P1_ELEC")                # kW
    Qp1_elec = p1_elec*3.6                                      # MJ/h
    Cp1_elec = p1_elec*ec.price["Electricity"]*time*3.6/(1e6)   # K$/year

    
    NT_LPC = simulation.get_variable("NT_LPC")          # -
    d_LPC = simulation.get_variable("d_LPC")            # m
    P_LPC = simulation.get_variable("P_LPC")*0.986923   # atm
    Tc_cin_LPC = 25    # °C
    Tc_cout_LPC = 35   # °C
    Tc_hin_LPC = simulation.get_variable_by_path("\\Data\\Blocks\\LPC\\Output\\B_TEMP\\2")              # °C
    Tc_hout_LPC = simulation.get_variable_by_path("\\Data\\Blocks\\LPC\\Output\\B_TEMP\\1")             # °C
    Tr_cin_LPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\LPC\\Output\\B_TEMP\\{NT_LPC-1}")    # °C
    Tr_cout_LPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\LPC\\Output\\B_TEMP\\{NT_LPC}")     # °C
    Tr_hin_LPC = 433 - 273.15   # °C
    Tr_hout_LPC = 432 - 273.15  # °C    
    Cvessel_LPC = eq.column_vessel(MaS, d_LPC, NT_LPC, P_LPC)   # k$
    Ctray_LPC = eq.column_plate(MaS, d_LPC, NT_LPC)             # k$
    Ccond_LPC = eq.heat_exchanger(MaS, Qc_LPC, Tc_hin_LPC, Tc_hout_LPC, Tc_cin_LPC, Tc_cout_LPC, P_LPC, False)  # k$
    Creb_LPC = eq.heat_exchanger(MaS, Qr_LPC, Tr_hin_LPC, Tr_hout_LPC, Tr_cin_LPC, Tr_cout_LPC, P_LPC, True)    # k$

    NT_HPC = simulation.get_variable("NT_HPC")          # - 
    d_HPC = simulation.get_variable("d_HPC")            # m
    P_HPC = simulation.get_variable("P_HPC")*0.986923   # atm
    Tc_cin_HPC = 25    # °C
    Tc_cout_HPC = 35   # °C
    Tc_hin_HPC = simulation.get_variable_by_path("\\Data\\Blocks\\HPC\\Output\\B_TEMP\\2")              # °C
    Tc_hout_HPC = simulation.get_variable_by_path("\\Data\\Blocks\\HPC\\Output\\B_TEMP\\1")             # °C
    Tr_cin_HPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\HPC\\Output\\B_TEMP\\{NT_HPC-1}")    # °C
    Tr_cout_HPC = simulation.get_variable_by_path(f"\\Data\\Blocks\\HPC\\Output\\B_TEMP\\{NT_HPC}")     # °C
    Tr_hin_HPC = 433 - 273.15   # °C
    Tr_hout_HPC = 432 - 273.15  # °C
    Cvessel_HPC = eq.column_vessel(MaS, d_HPC, NT_HPC, P_HPC)   # k$
    Ctray_HPC = eq.column_plate(MaS, d_HPC, NT_HPC)             # k$
    Ccond_HPC = eq.heat_exchanger(MaS, Qc_HPC, Tc_hin_HPC, Tc_hout_HPC, Tc_cin_HPC, Tc_cout_HPC, P_HPC, False)  # k$
    Creb_HPC = eq.heat_exchanger(MaS, Qr_HPC, Tr_hin_HPC, Tr_hout_HPC, Tr_cin_HPC, Tr_cout_HPC, P_HPC, True)    # k$

    
    Copex_LPC = (Ccw_LPC + Cs_LPC)/(1e3)    # K$/year
    Copex_HPC = (Ccw_HPC + Cs_HPC)/(1e3)    # K$/year
    TOC = Copex_LPC + Copex_HPC + Cp1_elec  # k$/year

    CLPC = Cvessel_LPC + Ctray_LPC + Ccond_LPC + Creb_LPC   # k$
    CHPC = Cvessel_HPC + Ctray_HPC + Ccond_HPC + Creb_HPC   # k$
    TCC = CLPC + CHPC # k$

    playback = 3
    TAC = TCC/playback + TOC # k$/year

    ei99_calc = EcoIndicator99()
    ei99_steam = ei99_calc.steam((Ms_LPC + Ms_HPC)*time)
    ei99_elect = ei99_calc.electricity(Qp1_elec*time)
    EI99 = ei99_steam + ei99_elect

    CO2_Oil = ec.co2_emission_fuel((Qr_LPC + Qr_HPC)*3600, "LPS", "Oil")    # kg/h
    CO2_NG = ec.co2_emission_fuel((Qr_LPC + Qr_HPC)*3600, "LPS", "NG")      # kg/h
    CO2_Ele = ec.co2_emission_elec(Qp1_elec/1e3)                            # kg/h

    # tracking data
    NF_F1 = simulation.get_variable("NF_F1")
    NF_D1 = simulation.get_variable("NF_D1")
    NF_D2 = simulation.get_variable("NF_D2")
    P_LPC = P_LPC/0.986923
    P_HPC = P_HPC/0.986923
    RR_LPC = simulation.get_variable("RR_LPC")
    RR_HPC = simulation.get_variable("RR_HPC")
    D1_ACN = simulation.get_variable("D1_ACN")
    D2_ACN =simulation.get_variable("D2_ACN")

    if complex == type(TAC):
         return np.inf
    tracking = [NT_LPC, NT_HPC, NF_F1, NF_D1, NF_D2, P_LPC, P_HPC, RR_LPC, RR_HPC,
                TAC, TCC, TOC, EI99, CO2_Oil, CO2_NG, CO2_Ele,
                d_LPC, d_HPC, Qr_LPC, Qr_HPC, Qc_LPC, Qc_HPC,
                B2_ACN, D1_ACN, D2_ACN,
                Tc_cin_LPC, Tc_cout_LPC, Tc_hin_LPC, Tc_hout_LPC, Tr_cin_LPC, Tr_cout_LPC, Tr_hin_LPC, Tr_hout_LPC,
                Tc_cin_HPC, Tc_cout_HPC, Tc_hin_HPC, Tc_hout_HPC, Tr_cin_HPC, Tr_cout_HPC, Tr_hin_HPC, Tr_hout_HPC]
    save(tracking)
    # end tracking

    return TAC

def save(tracking):
    data ={}
    for i, var in enumerate(tracking):
         data[tags[i]] = var

    historian.loc[len(historian)] = data

tags = ["NT_LPC", "NT_HPC", "NF_F1", "NF_D1", "NF_D2", "P_LPC(bar)", "P_HPC(bar)", "RR_LPC", "RR_HPC",
        "TAC(k$/year)", "TCC(k$)", "TOC(k$/year)", "EI99", "CO2_Oil(kg/h)", "CO2_NG(kg/h)", "CO2_Elec(kg/h)",
        "d_LPC(m)", "d_HPC(m)", "Qr_LPC(kW)", "Qr_HPC(kW)", "Qc_LPC(kW)", "Qc_HPC(kW)",
        "B2_ACN", "D1_ACN", "D2_ACN",
        "Tc_cin_LPC(°C)", "Tc_cout_LPC(°C)", "Tc_hin_LPC(°C)", "Tc_hout_LPC(°C)", "Tr_cin_LPC(°C)", "Tr_cout_LPC(°C)", "Tr_hin_LPC(°C)", "Tr_hout_LPC(°C)",
        "Tc_cin_HPC(°C)", "Tc_cout_HPC(°C)", "Tc_hin_HPC(°C)", "Tc_hout_HPC(°C)", "Tr_cin_HPC(°C)", "Tr_cout_HPC(°C)", "Tr_hin_HPC(°C)", "Tr_hout_HPC(°C)"]
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
    AspenVariable("B2_ACN","\\Data\\Streams\\B2\\Output\\MASSFRAC\\MIXED\\ACN"),
    AspenVariable("D1_ACN","\\Data\\Streams\\D1\\Output\\MASSFRAC\\MIXED\\ACN"),
    AspenVariable("D2_ACN","\\Data\\Streams\\D2\\Output\\MASSFRAC\\MIXED\\ACN")
]

try:
    simulation = AspenSimulation(simulation_file, variables)
    var = {
         "x":{
              "RR_LPC": [0.2, 0.60, 1.0],
              "RR_HPC": [0.2, 0.60, 1.0],
              "P_LPC":  [0.3, 0.75, 1.2],
              "P_HPC":  [2.5, 3.25, 4]
         },
         "y":{
              "NT_LPC": [10, 15, 20],
              "NT_HPC": [12, 17, 22],
              "NF_F1": [2, 5, 9],
              "NF_D1": [2, 5, 9],
              "NF_D2": [2, 5, 9]
         }
    }
    x0 = np.array([var["x"]["RR_LPC"][1], var["x"]["RR_HPC"][1], var["x"]["P_LPC"][1], var["x"]["P_HPC"][1]])
    y0 = np.array([var["y"]["NT_LPC"][1], var["y"]["NT_HPC"][1], var["y"]["NF_F1"][1], var["y"]["NF_D1"][1], var["y"]["NF_D2"][1]])
      
    bndsx = np.array([[var["x"]["RR_LPC"][0], var["x"]["RR_LPC"][2]], 
                      [var["x"]["RR_HPC"][0], var["x"]["RR_HPC"][2]], 
                      [var["x"]["P_LPC"][0],  var["x"]["P_LPC"][2]], 
                      [var["x"]["P_HPC"][0], var["x"]["P_HPC"][2]]])
    
    bndsy = np.array([[var["y"]["NT_LPC"][0], var["y"]["NT_LPC"][2]], 
                      [var["y"]["NT_HPC"][0], var["y"]["NT_HPC"][2]], 
                      [var["y"]["NF_F1"][0], var["y"]["NF_F1"][2]], 
                      [var["y"]["NF_D1"][0], var["y"]["NF_D1"][2]], 
                      [var["y"]["NF_D2"][0], var["y"]["NF_D2"][2]]])

    design_var = SimulatedAnnealingDesignVariable(x0, bndsx, y0, bndsy)

    conf = SimulatedAnnealingConfiguration(steps=50,
                                           mininum_temperature=1,
                                           cooling_schedule=0.025)

    optimizer = SimulatedAnnealing(conf)

    result = optimizer.solver(func, design_var)
    
finally:
    historian.to_csv(f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}-{simulation_file[:-4]}.csv")
    del simulation
      