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


class Splitter_8bit(Splitter):
    def __init__(self):
        super(Splitter_8bit, self).__init__(8)


class Splitter_32bit(Splitter):
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


#   A -|----|- sum
#   B -|    |- car
#   C -|----|
class FullAdder(Arithmetic, ABC):
    def __init__(self):
        super(FullAdder, self).__init__()
        self.input_names = ("A", "B", "C")
        self.ha = HalfAdder()
        self.or_gate = ORGate()

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = inputs["B"]
        C = inputs["C"]
        out_0 = self.ha.run({"A": A, "B": B})
        out_1 = self.ha.run({"A": out_0["sum"], "B": C})
        car = self.or_gate.run({"A": out_0["car"], "B": out_1["car"]})["C"]
        return {"sum": out_1["sum"], "car": car}


class FullAdder_multi_bits(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(FullAdder_multi_bits, self).__init__()
        self.input_names = ("A", "B", "C")
        self.num_bits = num_bits
        self.fa = FullAdder()
        self.splitter = Splitter(num_bits)
        self.hub = Hub(num_bits)

    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = inputs["B"]
        C = inputs["C"]
        assert C == 0 or C == 1
        A_split = self.splitter.run({"A": A})["B"]
        B_split = self.splitter.run({"A": B})["B"]
        s = []
        for a, b, in zip(A_split, B_split):
            out = self.fa.run({"A": a, "B": b, "C": C})
            C = out["car"]
            s.append(out["sum"])
        return {"sum": self.hub.run({"A": s})["B"], "car": C}


class FullAdder_8bit(FullAdder_multi_bits):
    def __init__(self):
        super(FullAdder_8bit, self).__init__(8)


class FullAdder_32bit(FullAdder_multi_bits):
    def __init__(self):
        super(FullAdder_32bit, self).__init__(32)


# A[in]: List[int]
# B[out]: List[int], length = pow(2, len(A))
class Decoder_multi_bits(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(Decoder_multi_bits, self).__init__()
        self.num_bits = num_bits
        self.hub = Hub(num_bits)

    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        assert isinstance(A, list)
        B = [0] * pow(2, len(A))
        index = self.hub.run({"A": A})["B"]
        B[index] = 1
        return {"B": B}


class Decoder_1bit(Decoder_multi_bits):
    def __init__(self):
        super(Decoder_1bit, self).__init__(1)


class Decoder_3bit(Decoder_multi_bits):
    def __init__(self):
        super(Decoder_3bit, self).__init__(3)


#       S
#       |
# A-->|---|-->B
#
# S = 0, B = 0
# S = 1, B = A
class SWC(Arithmetic, ABC):
    def __init__(self):
        super(SWC, self).__init__()
        self.input_names = ("A", "S")

    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        S = inputs["S"]
        if S == 0:
            B = 0
        else:
            B = A
        return {"B": B}


# B = -A
class NEG_multi_bits(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(NEG_multi_bits, self).__init__()
        self.num_bits = num_bits
        self.not_gate = NOTGate()
        self.adder = FullAdder_multi_bits(num_bits)

    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        not_out = self.not_gate.run({"A": A})["B"]
        B = self.adder.run({"A": not_out, "B": 1, "C": 0})["sum"]
        B = B & (pow(2, self.num_bits) - 1)
        return {"B": B}


class NEG_8bit(NEG_multi_bits):
    def __init__(self):
        super(NEG_8bit, self).__init__(8)


class NEG_32bit(NEG_multi_bits):
    def __init__(self):
        super(NEG_32bit, self).__init__(32)


# C = A - B
class Sub(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(Sub, self).__init__()
        self.num_bits = num_bits
        self.adder = FullAdder_multi_bits(num_bits)
        self.neg = NEG_multi_bits(num_bits)

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        neg_B = self.neg.run({"A": inputs["B"]})["B"]
        return self.adder.run({"A": inputs["A"], "B": neg_B, "C": 0})


# B = A << 1
class ShiftLeft(Arithmetic, ABC):
    def __init__(self):
        super(ShiftLeft, self).__init__()
        self.input_names = ("A",)

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        return {"B": inputs["A"] << 1}


# B = A >> 1
class ShiftRight(Arithmetic, ABC):
    def __init__(self):
        super(ShiftRight, self).__init__()
        self.input_names = ("A",)

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        return {"B": inputs["A"] >> 1}


class Mul(Arithmetic, ABC):
    def __init__(self, num_bits):
        super(Mul, self).__init__()
        self.input_names = ("A", "B")
        self.num_bits = num_bits
        self.shift_left = ShiftLeft()
        self.splitter = Splitter(num_bits)
        self.ha = HalfAdder()
        self.fa = FullAdder()
        self.swc = SWC()
        self.hub = Hub(num_bits)

    @check_inputs
    def run(self, inputs: Dict[str, Union[int, List[int]]]) -> Dict[str, Union[int, List[int]]]:
        A = inputs["A"]
        B = inputs["B"]
        tmp_mul_res = A
        mul_res = [0] * 2
        for i in range(self.num_bits):
            B_split = self.splitter.run({"A": B})["B"]
            if i == 0:
                mul_res[0] = self.swc.run({"A": tmp_mul_res, "S": B_split[i]})["B"]
            else:
                mul_res[1] = self.swc.run({"A": tmp_mul_res, "S": B_split[i]})["B"]

                add_res = []
                add_lhs = self.splitter.run({"A": mul_res[0]})["B"]
                add_rhs = self.splitter.run({"A": mul_res[1]})["B"]
                s = 0
                c = 0
                for n, (lhs, rhs) in enumerate(zip(add_lhs, add_rhs)):
                    if n == 0:
                        out = self.ha.run({"A": lhs, "B": rhs})
                    else:
                        out = self.fa.run({"A": lhs, "B": rhs, "C": c})
                    s = out["sum"]
                    c = out["car"]
                    add_res.append(s)
                mul_res[0] = self.hub.run({"A": add_res})["B"]
            tmp_mul_res = self.shift_left.run({"A": tmp_mul_res})["B"]
        return {"C": mul_res[0]}


def try_fulladder_8bit():
    samples = [{"A": 120, "B": 98}, ]
    C = [{"C": 1}]
    adder = FullAdder_multi_bits(8)
    for ab, car, in zip(samples, C):
        a = ab["A"]
        b = ab["B"]
        c = car["C"]
        output = adder.run({"A": a, "B": b, "C": c})["sum"]
        ref_sum = (a + b + c) % pow(2, 8)
        # ref_car = 1 if (a + b + c) > pow(2, num_bits) - 1 else 0
        print(f"output = {output}")
        print(f"ref_sum = {ref_sum}")
        assert output == ref_sum, f"{a} + {b} ==? {output}"


if __name__ == '__main__':
    try_fulladder_8bit()
