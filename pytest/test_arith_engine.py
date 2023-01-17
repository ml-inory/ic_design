from arith_engine import *
from utils import generate_samples


# op:
#   0   OR
#   1   NAND
#   2   NOR
#   3   AND
#   4   ADD
#   5   SUB
def test_arith_engine():
    samples = generate_samples(("A", "B"), -127, 128, sample_limit=1000)
    ops = generate_samples(("op",), 0, 6)
    ae = ArithEngine(8)
    for foo, bar in zip(samples, ops):
        A = foo["A"]
        B = foo["B"]
        op = bar["op"]
        out = ae.run({"A": A, "B": B, "op": op})["C"]
        if op == 0:
            ref_out = A | B
        elif op == 1:
            ref_out = ~(A & B)
        elif op == 2:
            ref_out = ~(A | B)
        elif op == 3:
            ref_out = A & B
        elif op == 4:
            ref_out = (A + B) % 256
        elif op == 5:
            ref_out = A - B
        elif op == 6:
            ref_out = (A * B) % 256
        assert out == ref_out or abs(out) + abs(ref_out) == pow(2, 8)