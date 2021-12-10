from diagram import Diagram
from utils import START_STATE, EPSILON
import anytree


class Parser:

    def __init__(self, scanner):
        self.firsts = dict()
        self.follows = dict()
        self.nonterminals = []
        self.create_first_follow()
        self.create_diagram()
        self.scanner = scanner
        self.token = self.scanner.get_next_token()
        self.errors = []
        self.root_node = None
        self.end_file = False

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
        self.root_node = start_diagram.start_process()

    def create_first_follow(self):
        first_file = open('first.txt', 'r')
        first_Lines = first_file.readlines()
        firsts = []
        for line in first_Lines:
            firsts.append(line.replace('\n', ''))

        follow_file = open('follow.txt', 'r')
        follow_Lines = follow_file.readlines()
        follows = []
        for line in follow_Lines:
            follows.append(line.replace('\n', ''))

        nonterminal_file = open('nonterminal.txt', 'r')
        nonterminal_Lines = nonterminal_file.readlines()
        for line in nonterminal_Lines:
            self.nonterminals.append(line.replace('\n', ''))

        counter = 0
        for nonter in self.nonterminals:
            self.firsts[nonter] = firsts[counter]
            self.follows[nonter] = follows[counter]
            counter += 1

    def chekFinal(self, counter, final):
        if (counter + 1) == final:
            return counter + 2
        return counter + 1

    def create_diagram(self):
        grammer_file = open('grammer.txt', 'r')
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
            counter = 0
            flag = 0
            final = 0
            for g in rights:
                space_split = g.split()
                if flag == 0:
                    final = len(space_split)
                    flag = 1

                if len(space_split) == 1:
                    zero[space_split[0]] = final
                else:
                    counter = self.chekFinal(counter, final)
                    zero[space_split[0]] = counter
                    for t in space_split[1:len(space_split) - 1]:
                        h = dict()
                        h[t] = counter + 1
                        states[counter] = h
                        counter = self.chekFinal(counter, final)
                    f = dict()
                    f[space_split[len(space_split) - 1]] = final
                    states[counter] = f

            states[0] = zero
            name = sl[0][:-1]
            # print(has_epsilon)
            diagram = Diagram(name, states, final, self.follows[name], self.firsts[name], self, has_epsilon)
            Diagram.all[name] = diagram
            # print()
