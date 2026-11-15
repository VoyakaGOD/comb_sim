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
        self.gates = []
        gates = schematics["gates"]
        drivers = schematics["drivers"]
        connections = {}
        for connection in drivers:
            dst = connection.split(".")
            if isinstance(drivers[connection], int):
                src = ("in", drivers[connection])
            else:
                src = drivers[connection].split(".")
                src[0] += "_out"
            connections.setdefault(dst[0], []).append(LogicConnection(
                "&" + dst[0] + "_in", int(dst[1]), src[0], int(src[1])
            ))
        for gate in schematics["gates"]:
            self.gates.append(LogicGate(gate, gates[gate], connections[gate]))
        self.output_connections = []
        for i, port in enumerate(schematics["output"]):
            src = port.split(".")
            self.output_connections.append(LogicConnection(
                "out", i, src[0] + "_out", int(src[1])
            ))

    # cached
    def get_ordered_list(self):
        return self.gates

    # cached
    def get_output_connections(self):
        return self.output_connections
