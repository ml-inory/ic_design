from logic_gates import *
from utils import generate_samples


def test_and_gate():
    and_gate = ANDGate()
    for sample in generate_samples(and_gate.input_names):
        ref_output = sample["A"] & sample["B"]
        output = and_gate.run(sample)
        assert output["C"] == ref_output


def test_not_gate():
    gate = NOTGate()
    for sample in generate_samples(gate.input_names):
        ref_output = ~sample["A"]
        output = gate.run(sample)
        assert output["B"] == ref_output


def test_nand_gate():
    gate = NANDGate()
    for sample in generate_samples(gate.input_names):
        ref_output = ~(sample["A"] & sample["B"])
        output = gate.run(sample)
        assert output["C"] == ref_output


def test_or_gate():
    gate = ORGate()
    for sample in generate_samples(gate.input_names):
        ref_output = sample["A"] | sample["B"]
        output = gate.run(sample)
        assert output["C"] == ref_output


def test_nor_gate():
    gate = NORGate()
    for sample in generate_samples(gate.input_names):
        ref_output = ~(sample["A"] | sample["B"])
        output = gate.run(sample)
        assert output["C"] == ref_output


def test_xor_gate():
    gate = XORGate()
    for sample in generate_samples(gate.input_names):
        ref_output = sample["A"] ^ sample["B"]
        output = gate.run(sample)
        assert output["C"] == ref_output


def test_xnor_gate():
    gate = XNORGate()
    for sample in generate_samples(gate.input_names):
        ref_output = ~(sample["A"] ^ sample["B"])
        output = gate.run(sample)
        assert output["C"] == ref_output