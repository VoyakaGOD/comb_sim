from dataclasses import dataclass

@dataclass
class LogicConnection:
    dst_name : str
    dst_index : int
    src_name : str
    src_index : int

@dataclass
class LogicGate:
    name : str
    gate_ref : str
    input_connections : list[LogicConnection]

class GateGraph:
    def __init__(self, schematics : dict):
        pass

    def get_ordered_list(self):
        return [LogicGate("A", "and", [LogicConnection("A_in", 0, "in", 0), LogicConnection("A_in", 1, "in", 1)])]

    def get_output_connections(self):
        return [LogicConnection("out", 0, "A", 0)]
