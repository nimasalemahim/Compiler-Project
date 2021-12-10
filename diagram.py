from utils import *
import anytree


class Diagram:
    all = dict()

    def __init__(self, name, states, final, follow, first, parser):
        self.name = name
        self.states = states
        self.final = final
        self.first = first
        self.follow = follow
        self.parser = parser

    def start_process(self, parent=None):
        state = 0
        node = anytree.Node(self.name, parent)
        row, (type, token) = self.parser.token
        check_token = type if type in [ID, NUM] else token
        if check_token in self.first:
            while state != self.final:
                transitions = self.states.get(state)
                for tra in transitions.keys():
                    if tra in self.parser.nonterminals:
                        diagram = self.all.get(tra)
                        if check_token in diagram.first or (check_token in diagram.follow and EPSILON in diagram.first):
                            # print(f'add to tree {tra}')
                            state = transitions.get(tra)
                            diagram.start_process(node)
                    else:
                        if check_token == tra:
                            # add to tree
                            # print(f'add to tree {tra}')
                            anytree.Node(f'({type}, {token})', node)
                            state = transitions.get(tra)
                            self.parser.next_token()
                            row, (type, token) = self.parser.token
                            check_token = type if type in [ID, NUM] else token
                        else:
                            pass # missing error token
        else:
            if check_token in self.follow:
                if EPSILON in self.first:
                    # add epsilon to tree
                    print(f'add to tree epsilon')
                    pass
                else:
                    pass  # missing error self.name
            else:
                pass  # illegal error token

        return node
