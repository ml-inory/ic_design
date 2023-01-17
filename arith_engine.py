from logic_gates import *
from arithmetic import *


# op[in]: 0-3
# A[in]
# B[in]
# C[out] = A op B
#
# op:
#   0   OR
#   1   NAND
#   2   NOR
#   3   AND
#   4   ADD
#   5   SUB
class ArithEngine:
    OPS = {
        "OR": 0,
        "NAND": 1,
        "NOR": 2,
        "AND": 3,
        "ADD": 4,
        "SUB": 5,
        "MUL": 6,
    }

    def __init__(self, num_bits):
        self.num_bits = num_bits

        self.splitter = Splitter_8bit()
        self.decoder = Decoder_3bit()
        self.swc = SWC()

        self.or_gate = ORGate()
        self.nand_gate = NANDGate()
        self.nor_gate = NORGate()
        self.and_gate = ANDGate()
        self.adder = FullAdder_multi_bits(num_bits)
        self.suber = Sub(num_bits)
        self.mul = Mul(num_bits)

        self.or_gate_4way = ORGate_4way()

    def run(self, inputs):
        A = inputs["A"]
        B = inputs["B"]
        op = self.decoder.run(
            {"A": self.splitter.run({"A": inputs["op"]})["B"][:3]}
        )["B"]

        or_out = self.or_gate.run({"A": A, "B": B})["C"]
        nand_out = self.nand_gate.run({"A": A, "B": B})["C"]
        nor_out = self.nor_gate.run({"A": A, "B": B})["C"]
        and_out = self.and_gate.run({"A": A, "B": B})["C"]
        add_out = self.adder.run({"A": A, "B": B, "C": 0})["sum"]
        sub_out = self.suber.run({"A": A, "B": B, "C": 0})["sum"]
        mul_out = self.mul.run({"A": A, "B": B})["C"]

        outs = [
            self.swc.run({"A": or_out, "S": op[self.OPS["OR"]]})["B"],
            self.swc.run({"A": nand_out, "S": op[self.OPS["NAND"]]})["B"],
            self.swc.run({"A": nor_out, "S": op[self.OPS["NOR"]]})["B"],
            self.swc.run({"A": and_out, "S": op[self.OPS["AND"]]})["B"],
            self.swc.run({"A": add_out, "S": op[self.OPS["ADD"]]})["B"],
            self.swc.run({"A": sub_out, "S": op[self.OPS["SUB"]]})["B"],
            self.swc.run({"A": mul_out, "S": op[self.OPS["MUL"]]})["B"],
        ]

        or_0 = self.or_gate_4way.run({"A": outs[:4]})["B"]
        or_1 = self.or_gate_4way.run({"A": [or_0, outs[4], outs[5], outs[6]]})["B"]
        return {"C": or_1}
