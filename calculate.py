import state

max_depth = 10
max_breadth = 10

def successors(prev):
    if prev.depth >= max_depth:
        return []
    elif prev.node == state.nodes.act:
        result = []
        for a in state.actions:
            new = state.state(prev)
            if a(new):
                result.append(new)
        return result
    elif prev.node == state.nodes.choose:
        result = []
        for c in state.choices:
            new = state.state(prev)
            if c(new):
                result.append(new)
        return result