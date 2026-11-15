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
        gates = schematics["gates"]
        drivers = schematics["drivers"]
        logic_connections = {}
        top_connections = {}
        indeg = {gate: 0 for gate in gates}
        for connection in drivers:
            dst = connection.split(".")
            src = str(drivers[connection]).split(".")
            if len(src) == 1:
                src = ("in", drivers[connection])
            else:
                indeg[dst[0]] += 1
                top_connections.setdefault(src[0], []).append(dst[0])
                src[0] += "_out"
            logic_connections.setdefault(dst[0], []).append(LogicConnection(
                "&" + dst[0] + "_in", int(dst[1]), src[0], int(src[1])
            ))
        self.gates = []
        queue = {}
        ready_gates = []
        for gate in gates:
            item = LogicGate(gate, gates[gate], logic_connections[gate])
            if indeg[gate] == 0:
                ready_gates.append(item)
            else:
                queue[gate] = item
        while len(ready_gates) > 0:
            item = ready_gates.pop()
            self.gates.append(item)
            for connection in top_connections.setdefault(item.name, []):
                indeg[connection] -= 1
                if indeg[connection] == 0:
                    ready_gates.append(queue.pop(connection))
        self.output_connections = []
        for i, port in enumerate(schematics["output"]):
            src = str(port).split(".")
            if len(src) == 1:
                self.output_connections.append(LogicConnection(
                    "out", i, "in", int(port)
                ))
            else:
                self.output_connections.append(LogicConnection(
                    "out", i, src[0] + "_out", int(src[1])
                ))

    def get_ordered_list(self):
        return self.gates

    def get_output_connections(self):
        return self.output_connections
