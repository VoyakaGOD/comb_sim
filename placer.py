from gate_graph import *
from typing import Callable

class PlacerBase:
    def __init__(self, write : Callable[[str], int]):
        self.write = write

    def get_args(self) -> str:
        raise NotImplementedError

    def place_gate_input(self, gate : LogicGate) -> None:
        raise NotImplementedError

    def place_connection(self, connection : LogicConnection, out : bool) -> None:
        raise NotImplementedError

    def place_gate_calc(self, gate : LogicGate) -> None:
        raise NotImplementedError

    def place_gate(self, gate : LogicGate):
        self.place_gate_input(gate)
        for connection in gate.input_connections:
            self.place_connection(connection, False)
        self.place_gate_calc(gate)

    def __call__(self, gg : GateGraph):
        self.write(f"void calc({self.get_args()})\n{{\n")
        for gate in gg.get_ordered_list():
            self.place_gate(gate)
        for connection in gg.get_output_connections():
            self.place_connection(connection, True)
        self.write("}\n")

class DefinedPlacer(PlacerBase):
    def get_args(self):
        return "const uint8_t in [], uint8_t out []"

    def place_gate_input(self, gate: LogicGate):
        self.write(f"    uint64_t {gate.name}_in = 0;\n")

    def place_connection(self, connection : LogicConnection, out : bool):
        func = "move_bit" if out else "set_bit"
        self.write(f"    {func}({connection.dst_name}, "
            f"{connection.dst_index}, "
            f"{connection.src_name}, "
            f"{connection.src_index});\n")

    def place_gate_calc(self, gate : LogicGate):
        self.write(f"    const uint8_t *{gate.name}_out = "
            f"calc_gate(&gate_{gate.gate_ref}_table[0][0], "
            f"GATE_{gate.gate_ref}_OUTW, {gate.name}_in);\n\n")

class UndefinedPlacer(PlacerBase):
    def __init__(self, write : Callable[[str], int], out_u_scale : int = 1):
        super().__init__(write)
        self.out_u_scale = out_u_scale

    def get_args(self):
        return ("const uint8_t in [], const uint8_t in_u [], "
            "uint8_t out [], uint8_t out_u []")
    
    def place_gate_input(self, gate: LogicGate):
        self.write(f"    uint64_t {gate.name}_in = 0;\n")
        self.write(f"    uint64_t {gate.name}_in_u = 0;\n")
        if self.out_u_scale == 1:
            self.write(f"    uint8_t {gate.name}_out_u [GATE_{gate.gate_ref}_OUTW] = {{0}};\n")
        else:
            self.write(f"    uint8_t {gate.name}_out_u "
                f"[{self.out_u_scale}*GATE_{gate.gate_ref}_OUTW] = {{0}};\n")

    def place_connection(self, connection : LogicConnection, out : bool):
        func = "move_bit" if out else "set_bit"
        self.write(f"    {func}({connection.dst_name}, "
            f"{connection.dst_index}, "
            f"{connection.src_name}, "
            f"{connection.src_index});\n")
        self.write(f"    {func}({connection.dst_name}_u, "
            f"{connection.dst_index}, "
            f"{connection.src_name}_u, "
            f"{connection.src_index});\n")

    def place_gate_calc(self, gate : LogicGate):
        self.write(f"    const uint8_t *{gate.name}_out = "
            f"calc_gate(&gate_{gate.gate_ref}_table[0][0], "
            f"GATE_{gate.gate_ref}_OUTW, {gate.name}_in, "
            f"{gate.name}_in_u, {gate.name}_out_u);\n\n")
