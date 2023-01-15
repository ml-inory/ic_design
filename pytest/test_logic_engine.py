from logic_engine import *
from utils import generate_samples


# op:
#   0   OR
#   1   NAND
#   2   NOR
#   3   AND
def test_logic_engine():
    samples = generate_samples(("A", "B"), 0, 255, sample_limit=10000)
    ops = generate_samples(("op",), 0, 3)
    le = LogicEngine()
    for foo, bar in zip(samples, ops):
        A = foo["A"]
        B = foo["B"]
        op = bar["op"]
        out = le.run({"A": A, "B": B, "op": op})["C"]
        if op == 0:
            ref_out = A | B
        elif op == 1:
            ref_out = ~(A & B)
        elif op == 2:
            ref_out = ~(A | B)
        else:
            ref_out = A & B
        assert ref_out == out