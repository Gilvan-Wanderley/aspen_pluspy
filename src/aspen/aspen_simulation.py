import win32com.client as win32
import os
from .utils.aspen_variable import AspenVariable


class AspenSimulation:
    def __init__(self, file_name: str, variables: list[AspenVariable],  visibility=False) -> None:
        try:
            self.file_path = os.path.join(os.getcwd(), "simulation", file_name)
            print(f"simulation path: {self.file_path}")
            print("Opening simulation...")
            self.file_name = file_name
            self.aspen = win32.gencache.EnsureDispatch("Apwn.Document")
            self.aspen.InitFromArchive2(self.file_path)
            self.aspen.Visible = visibility
            print("Simulation opened with success.")
            print("Start Test - Run simulation.")
            self.aspen.Engine.Run2()
            print("End Test - Run simulation (Success).")
            print("Start Test - Check variables.")
            self.vars = {}
            for var in variables:
                print(f"Checking variable ({var.name} - {var.path})")
                node = self.aspen.Application.Tree.FindNode(var.path)
                print(f"Variable {var.name} found ({node.Name}). Registering variable.")
                self.vars[var.name] = {"path": var.path,
                                       "unit": node.UnitString,
                                       "name": node.Name}
            print("End Test - Check variables (Success).")
        except:
            self.__del__()            

    def __del__(self) -> None:
        self.aspen.Application.Quit()
        print("Quit simulation.")

    def visible(self, value: bool) -> None:
        self.aspen.Visible = value

    def run(self) -> None:
        self.aspen.Engine.Run2()

    def get_variable(self, name: str) -> float|int:
        path = self.vars[name]["path"]
        return self.aspen.Application.Tree.FindNode(path).Value
    
    def set_variable(self, name: str, value: float|int) -> None:
        path = self.vars[name]["path"]
        self.aspen.Application.Tree.FindNode(path).Value = value

    def get_variable_by_path(self, path: str) -> float|int:
        return self.aspen.Application.Tree.FindNode(path).Value
    
    def set_variable_by_path(self, path: str, value: float|int) -> None:
        self.aspen.Application.Tree.FindNode(path).Value = value

    def status(self) -> bool:
        status = self.aspen.Application.Tree.FindNode("\\Data\\Results Summary\\Run-Status\\Output\\PER_ERROR").Elements.Count
        if status == 0:
            return True
        else:
            self.aspen.Reinit()
            return  False
        
    def reinit(self) -> None:
        self.aspen.Reinit()