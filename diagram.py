from utils import *
import anytree


class Diagram:
    all = dict()

    def __init__(self, name, states, final, follow, first, parser, has_epsilon):
        self.name = name
        self.states = states
        self.final = final
        self.first = first
        self.follow = follow
        self.parser = parser
        self.has_epsilon = has_epsilon

    # def get_token(self):
    #     row, (type, token) = self.parser.token
    #     check_token = type if type in [ID, NUM] else token
    def start_process(self, parent=None):
        state = 0
        node = anytree.Node(self.name, parent)
        row, (type, token) = self.parser.token
        check_token = type if type in [ID, NUM] else token
        if check_token in self.first:
            while state != self.final:
                transitions = self.states.get(state)
                # if self.name == 'Factor':
                #     print(state, transitions, self.states)
                for tra in transitions.keys():
                    if tra in self.parser.nonterminals:
                        diagram = self.all.get(tra)
                        if check_token in diagram.first or (check_token in diagram.follow and EPSILON in diagram.first):
                            # print(f'add to tree {tra}')

                            state = transitions.get(tra)
                            diagram.start_process(node)
                            row, (type, token) = self.parser.token
                            check_token = type if type in [ID, NUM] else token
                            break
                    else:
                        if check_token == tra:
                            # add to tree
                            # print(f'add to tree {tra}')
                            string = check_token if check_token == '$' else f'({type}, {token})'
                            anytree.Node(string, node)
                            state = transitions.get(tra)
                            self.parser.next_token()
                            if self.name == 'Factor':
                                print(tra, state, self.states)
                            # print(self.parser.token)
                            row, (type, token) = self.parser.token
                            check_token = type if type in [ID, NUM] else token
                            break
                        else:
                            pass  # missing error token
        else:
            if check_token in self.follow:
                if EPSILON in self.first:
                    if self.has_epsilon:
                        # add epsilon to tree
                        # print(f'add to tree epsilon')
                        anytree.Node('epsilon', node)
                    else:
                        while state != self.final:
                            transitions = self.states.get(state)
                            for tra in transitions.keys():
                                if tra in self.parser.nonterminals:
                                    # if self.name == 'Term-prime':
                                    #     print(tra)
                                    # print(tra)
                                    # print(self.name, self.states, self.has_epsilon)
                                    # print(transitions.keys(), self.name)
                                    diagram = self.all.get(tra)
                                    if EPSILON in diagram.first:
                                        diagram.start_process(node)
                                        state = transitions.get(tra)
                                        break

                else:
                    pass  # missing error self.name
            else:
                pass  # illegal error token

        return node
