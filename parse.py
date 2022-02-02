from diagram import Diagram
from utils import START_STATE, EPSILON, DEBUG
import anytree
from code_generator import CodeGenerator

class Parser:

    def __init__(self, scanner, code_generator):
        self.firsts = dict()
        self.follows = dict()
        self.test_file = ''
        if DEBUG:
            self.test_file = '_test'
        self.nonterminals = []
        self.create_first_follow()
        self.create_diagram()
        self.scanner = scanner
        self.token = self.scanner.get_next_token()
        self.errors = []
        self.root_node = None
        self.end_file = False
        Diagram.code_generator_class = code_generator

    def save_errors(self, file):
        with open(file, 'w') as f:
            if self.errors:
                f.write('\n'.join(f'#{a} : syntax error, {b} {c}' for a, b, c in self.errors))
            else:
                f.write('There is no syntax error.')

    def save_tree(self, file):
        with open(file, 'w') as f:
            f.write(anytree.RenderTree(self.root_node).by_attr(attrname="name"))

    def next_token(self):
        self.token = self.scanner.get_next_token()

    def start(self):
        start_diagram = Diagram.all.get(START_STATE)
        # for i in Diagram.all:
        #     print(i)
        #     print(Diagram.all[i].states)
        #     print(Diagram.all[i].actions)
        self.root_node = start_diagram.start_process()

    def create_first_follow(self):
        first_file = open(f'first{self.test_file}.txt', 'r')
        first_Lines = first_file.readlines()
        firsts = []
        for line in first_Lines:
            firsts.append(line.replace('\n', ''))

        follow_file = open(f'follow{self.test_file}.txt', 'r')
        follow_Lines = follow_file.readlines()
        follows = []
        for line in follow_Lines:
            follows.append(line.replace('\n', ''))

        nonterminal_file = open(f'nonterminal{self.test_file}.txt', 'r')
        nonterminal_Lines = nonterminal_file.readlines()
        for line in nonterminal_Lines:
            self.nonterminals.append(line.replace('\n', ''))

        counter = 0
        for nonter in self.nonterminals:
            self.firsts[nonter] = firsts[counter]
            self.follows[nonter] = follows[counter]
            counter += 1

    def check_actions(self, i, actions, j):
        if i not in actions.keys():
            actions[i] = dict()
        if j not in actions[i].keys():
            actions[i][j] = []
        return actions

    def chekFinal(self, counter, final):
        if (counter + 1) == final:
            return counter + 2
        return counter + 1

    def create_diagram(self):
        grammer_file = open(f'grammer{self.test_file}.txt', 'r')
        grammer_lines = grammer_file.readlines()
        for line in grammer_lines:
            has_epsilon = False
            sl = line.split('->')
            rights = sl[1].split('|')
            for g in rights:
                if g.replace(' ', '').replace('\n', '') == EPSILON:
                    has_epsilon = True
                l = g.split()
            states = dict()
            zero = dict()
            actions = dict()
            counter = 0
            flag = 0
            final = 0
            for g in rights:
                space_split = g.split()
                mai = 0

                non_act = []
                for i in space_split:
                    if i[0] != '#':
                        mai += 1
                        non_act.append(i)

                if flag == 0:
                    final = mai
                    flag = 1

                if mai == 1:
                    ze = 0
                    for t in space_split:
                        if t[0] != '#':
                            ze = 1
                            zero[t] = final
                        else:
                            if ze == 0:
                                self.check_actions(0, actions, non_act[0])
                                actions[0][non_act[0]].append(t[1:])
                            else:
                                self.check_actions(final, actions, non_act[0])
                                actions[final][non_act[0]].append(t[1:])
                else:
                    fg = 0
                    for t in space_split:
                        if t[0] != '#':
                            fg += 1

                        if fg == 0:
                            self.check_actions(0, actions, non_act[0])
                            actions[0][non_act[0]].append(t[1:])

                        elif fg == 1:
                            if t[0] == '#':
                                self.check_actions(counter, actions, non_act[fg])
                                actions[counter][non_act[fg]].append(t[1:])
                            else:

                                counter = self.chekFinal(counter, final)
                                zero[t] = counter

                        elif fg == mai:
                            if t[0] == '#':
                                self.check_actions(final, actions, non_act[fg - 1])
                                actions[final][non_act[fg - 1]].append(t[1:])
                            else:
                                f = dict()
                                f[t] = final
                                states[counter] = f
                        else:
                            if t[0] == '#':
                                self.check_actions(counter, actions, non_act[fg])
                                actions[counter][non_act[fg]].append(t[1:])
                            else:
                                h = dict()
                                h[t] = counter + 1
                                states[counter] = h
                                counter = self.chekFinal(counter, final)

            states[0] = zero
            name = sl[0][:-1]
            # print(has_epsilon)
            diagram = Diagram(name, states, final, self.follows[name], self.firsts[name], self, has_epsilon, actions)
            Diagram.all[name] = diagram
            # print()
