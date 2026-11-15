from gate_graph import *

class PlacerBase:
    def place_gate_input(self, gate : LogicGate):
        raise NotImplementedError

    def place_connection(self, connection : LogicConnection, out : bool):
        raise NotImplementedError

    def place_gate_calc(self, gate : LogicGate):
        raise NotImplementedError

    def place_gate(self, gate : LogicGate):
        self.place_gate_input(gate)
        for connection in gate.input_connections:
            self.place_connection(connection, False)
        self.place_gate_calc(gate)

    def __call__(self, gg : GateGraph):
        for gate in gg.get_ordered_list():
            self.place_gate(gate)
        for connection in gg.get_output_connections():
            self.place_connection(connection, True)

class DefinedPlacer(PlacerBase):
    pass

class UndefinedPlacer(PlacerBase):
    pass
