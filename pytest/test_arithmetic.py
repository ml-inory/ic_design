from utils import generate_samples
from arithmetic import *


def helper_fulladder_num_bits(num_bits):
    samples = generate_samples(("A", "B"), 0, pow(2, num_bits) - 1)
    C = generate_samples(("C",), 0, 1)
    adder = FullAdder_multi_bits(num_bits)
    for ab, car, in zip(samples, C):
        a = ab["A"]
        b = ab["B"]
        c = car["C"]
        output = adder.run({"A": a, "B": b, "C": c})
        ref_sum = (a + b + c) % pow(2, num_bits)
        ref_car = 1 if (a + b + c) > pow(2, num_bits) - 1 else 0
        assert ref_sum == output["sum"]
        assert ref_car == output["car"]


def test_fulladder_8bit():
    helper_fulladder_num_bits(8)


def test_fulladder_32bit():
    helper_fulladder_num_bits(32)