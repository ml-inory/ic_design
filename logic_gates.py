from abc import abstractmethod, ABC
from typing import Dict
from utils import check_inputs


class Gate:
    def __init__(self):
        self.input_names = ("A", "B")

    @abstractmethod
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        pass


# B = NOT(A)
class NOTGate(Gate, ABC):
    def __init__(self):
        super(NOTGate, self).__init__()
        self.input_names = ("A",)

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        return {"B": ~inputs["A"]}


# C = NAND(A, B)
class NANDGate(Gate, ABC):
    def __init__(self):
        super().__init__()
        self.input_names = ("A", "B")

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        return {"C": ~(inputs["A"] & inputs["B"])}


# C = A AND B
class ANDGate(Gate, ABC):
    def __init__(self):
        super().__init__()
        self.input_names = ("A", "B")
        self.nand_gate = NANDGate()
        self.not_gate = NOTGate()

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        return {"C": self.not_gate.run({"A": self.nand_gate.run(inputs)["C"]})["B"]}


class ORGate(Gate, ABC):
    def __init__(self):
        super(ORGate, self).__init__()
        self.input_names = ("A", "B")
        self.nand_gate = NANDGate()
        self.not_gate = NOTGate()

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        not_out_A = self.not_gate.run({"A": inputs["A"]})["B"]
        not_out_B = self.not_gate.run({"A": inputs["B"]})["B"]
        out = self.nand_gate.run({"A": not_out_A, "B": not_out_B})["C"]
        return {"C": out}


class NORGate(Gate, ABC):
    def __init__(self):
        super(NORGate, self).__init__()
        self.or_gate = ORGate()
        self.not_gate = NOTGate()

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        or_out = self.or_gate.run(inputs)["C"]
        not_out = self.not_gate.run({"A": or_out})["B"]
        return {"C": not_out}


class XORGate(Gate, ABC):
    def __init__(self):
        super(XORGate, self).__init__()
        self.not_gate = NOTGate()
        self.and_gate = ANDGate()
        self.or_gate = ORGate()

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        A = inputs["A"]
        B = inputs["B"]
        not_A = self.not_gate.run({"A": A})["B"]
        not_B = self.not_gate.run({"A": B})["B"]
        and_0 = self.and_gate.run({"A": not_A, "B": B})["C"]
        and_1 = self.and_gate.run({"A": not_B, "B": A})["C"]
        out = self.or_gate.run({"A": and_0, "B": and_1})["C"]
        return {"C": out}


class XNORGate(Gate, ABC):
    def __init__(self):
        super(XNORGate, self).__init__()
        self.xor_gate = XORGate()
        self.not_gate = NOTGate()

    @check_inputs
    def run(self, inputs: Dict[str, int]) -> Dict[str, int]:
        A = inputs["A"]
        B = inputs["B"]
        xor_out = self.xor_gate.run({"A": A, "B": B})["C"]
        out = self.not_gate.run({"A": xor_out})["B"]
        return {"C": out}