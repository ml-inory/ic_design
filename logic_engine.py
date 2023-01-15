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
class LogicEngine:
    def __init__(self):
        self.splitter = Splitter_8bit()
        self.decoder = Decoder_3bit()
        self.swc = SWC()

        self.or_gate = ORGate()
        self.nand_gate = NANDGate()
        self.nor_gate = NORGate()
        self.and_gate = ANDGate()

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

        out = [
            self.swc.run({"A": or_out, "S": op[0]})["B"],
            self.swc.run({"A": nand_out, "S": op[1]})["B"],
            self.swc.run({"A": nor_out, "S": op[2]})["B"],
            self.swc.run({"A": and_out, "S": op[3]})["B"]
        ]
        return {"C":
                self.or_gate_4way.run({"A": out})["B"]}
