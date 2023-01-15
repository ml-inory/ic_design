import random


def check_inputs(func):
    def wrapper(*args, **kw):
        self = args[0]
        inputs = args[1]
        input_names = self.input_names
        for name in input_names:
            assert name in inputs.keys()
        return func(*args, **kw)

    return wrapper


def generate_samples(input_names, min_val=0, max_val=1, sample_limit=1000):
    samples = []
    for i in range(sample_limit):
        inputs = {}
        for name in input_names:
            inputs[name] = random.randint(min_val, max_val)
        samples.append(inputs)
    return samples
