from logic_gates import *
from utils import check_inputs
from abc import abstractmethod, ABC
from typing import Dict, List, Union


class Arithmetic:
    def __init__(self):
        self.input_names = ("A", "B")

    @abstractmethod
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        pass


# B = Splitter(A)
# B: list[int]
class Splitter(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(Splitter, self).__init__()
        self.input_names = ("A",)
        self.num_bits = num_bits

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = []
        for i in range(self.num_bits):
            B.append((A >> i) & 1)
        return {"B": B}


class Splitter_8bit(Arithmetic, ABC):
    def __init__(self):
        super(Splitter_8bit, self).__init__(8)


class Splitter_32bit(Arithmetic, ABC):
    def __init__(self):
        super(Splitter_32bit, self).__init__(32)


# B = Splitter(A)
# A: list[int]
# B: int
class Hub(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(Hub, self).__init__()
        self.input_names = ("A",)
        self.num_bits = num_bits

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = 0
        for i in range(self.num_bits):
            B += A[i] << i
        return {"B": B}


class Hub_8bit(Hub):
    def __init__(self):
        super(Hub_8bit, self).__init__(8)


class Hub_32bit(Hub):
    def __init__(self):
        super(Hub_32bit, self).__init__(32)


# SUM = XOR(A, B)
# CAR = AND(A, B)
class HalfAdder(Arithmetic, ABC):
    def __init__(self):
        super(HalfAdder, self).__init__()
        self.xor_gate = XORGate()
        self.and_gate = ANDGate()

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        return {
                "sum": self.xor_gate.run(inputs)["C"],
                "car": self.and_gate.run(inputs)["C"]
                }


# SUM, CAR = FullAdder(A, B, C)
class FullAdder(Arithmetic, ABC):
    def __init__(self):
        super(FullAdder, self).__init__()
        self.input_names = ("A", "B", "C")
        self.half_adder = HalfAdder()
        self.or_gate = ORGate()

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = inputs["B"]
        C = inputs["C"]
        assert C == 0 or C == 1
        out_0 = self.half_adder.run({"A": A, "B": B})
        out_1 = self.half_adder.run({"A": out_0["sum"], "B": C})
        c_out = self.or_gate.run({"A": out_0["car"], "B": out_1["car"]})["C"]
        return {"sum": out_1["sum"], "car": c_out}


class FullAdder_multi_bits(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(FullAdder_multi_bits, self).__init__()
        self.input_names = ("A", "B", "C")
        self.num_bits = num_bits
        self.adder = FullAdder()
        self.splitter = Splitter(num_bits)
        self.hub = Hub(num_bits)

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = self.splitter.run({"A": inputs["A"]})["B"]
        B = self.splitter.run({"A": inputs["B"]})["B"]
        C = inputs["C"]
        assert C == 0 or C == 1
        sum_output = []
        car = 0
        for i in range(self.num_bits):
            tmp_output = self.adder.run({"A": A[i], "B": B[i], "C": C})
            C = tmp_output["car"]
            sum_output.append(tmp_output["sum"])
            if i == self.num_bits - 1:
                car = C
        return {"sum": self.hub.run({"A": sum_output})["B"], "car": car}


class FullAdder_8bit(FullAdder_multi_bits):
    def __init__(self):
        super(FullAdder_8bit, self).__init__(8)


class FullAdder_32bit(FullAdder_multi_bits):
    def __init__(self):
        super(FullAdder_32bit, self).__init__(32)