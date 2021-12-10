
class Diagram:
    all = []
    def __init__(self, name, states, final, follow, first):
        self.name = name
        self.states = states
        self.final = final
        self.first = first
        self.follow = follow
