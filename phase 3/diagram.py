from utils import *
import anytree


class Diagram:
    all = dict()
    code_generator_class = None

    def __init__(self, name, states, final, follow, first, parser, has_epsilon, actions):
        self.name = name
        self.states = states
        # self.actions = {
        #     '1': {
        #         'id': 'action'
        #     }
        # }
        self.final = final
        self.first = first
        self.follow = follow
        self.parser = parser
        self.has_epsilon = has_epsilon
        self.actions = actions

    def do_actions(self, state, tra, token):
        # pass
        # print(state, tra, self.actions)
        action = self.actions.get(state, None)
        # print(action)
        if action:
            ac = action.get(tra, None)
            if not ac:
                return
            # print(state, tra, token)
            # print(self.name, self.actions, self.states)
            # print(ac, action, tra)
            for i in ac:
                # print(i)
                Diagram.code_generator_class.generate_code(i, token)

    def start_process(self, parent=None):
        state = 0
        row, (type, token) = self.parser.token
        check_token = type if type in [ID, NUM] else token
        node = None
        if check_token in self.first:
            node = anytree.Node(self.name, parent)
            while state != self.final:
                transitions = self.states.get(state)
                for tra in transitions.keys():
                    if tra in self.parser.nonterminals:
                        diagram = self.all.get(tra)
                        if (check_token in diagram.first or (
                                check_token in diagram.follow and EPSILON in diagram.first)) or state != 0:
                            # code generate
                            # print(tra, state, self.parser.token[1][1])
                            self.do_actions(state, tra, self.parser.token[1][1])
                            state = transitions.get(tra)
                            diagram.start_process(node)
                            if self.final == state:
                                self.do_actions(state, tra, self.parser.token[1][1])
                            if self.parser.end_file:
                                return node
                            row, (type, token) = self.parser.token
                            check_token = type if type in [ID, NUM] else token
                            break
                    else:
                        if check_token == tra:
                            string = check_token if check_token == '$' else f'({type}, {token})'
                            anytree.Node(string, node)
                            # code generate

                            self.do_actions(state, tra, self.parser.token[1][1])
                            state = transitions.get(tra)
                            if self.final == state:
                                self.do_actions(state, tra, self.parser.token[1][1])
                            self.parser.next_token()
                            row, (type, token) = self.parser.token
                            check_token = type if type in [ID, NUM] else token
                            break
                        else:
                            if state != 0:
                                state = transitions.get(tra)
                                self.parser.errors.append((row, 'missing', tra))
                                break



        else:
            if check_token in self.follow:
                if EPSILON in self.first:
                    node = anytree.Node(self.name, parent)
                    if self.has_epsilon:
                        anytree.Node('epsilon', node)
                    else:
                        while state != self.final:
                            transitions = self.states.get(state)
                            for tra in transitions.keys():
                                if tra in self.parser.nonterminals:
                                    diagram = self.all.get(tra)
                                    if EPSILON in diagram.first:
                                        # code generate
                                        self.do_actions(state, tra, self.parser.token[1][1])
                                        state = transitions.get(tra)
                                        diagram.start_process(node)
                                        if self.final == state:
                                            self.do_actions(state, tra, self.parser.token[1][1])
                                        if self.parser.end_file:
                                            return node
                                        break

                else:
                    self.parser.errors.append((row, 'missing', self.name))
            else:
                if check_token == '$':
                    self.parser.errors.append((row, 'Unexpected', 'EOF'))
                    self.parser.end_file = True
                else:
                    self.parser.errors.append((row, 'illegal', check_token))
                    self.parser.next_token()
                    self.start_process(parent)

        return node
