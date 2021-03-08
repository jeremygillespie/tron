class state:
    def __init__(self, prev):
        if prev is None:
            self.depth = 0
            self.value = 0
        else:
            self.depth = prev.depth + 1
            self.value = prev.value

def deterministic(prev):
    new = state(prev)
    if new.value == 3:
        new.value = 0
    return [new], [1.0]

def stochastic(prev):
    good = state(prev)
    good.value += 2
    bad = state(prev)
    bad.value -= 2
    return [good, bad], [0.5, 0.5]

actions = [
    deterministic,
    stochastic
    ]