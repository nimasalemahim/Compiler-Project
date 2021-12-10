from diagram import Diagram


class Parser:
    def __init__(self):
        self.firsts = dict()
        self.follows = dict()
        self.create_first_follow()
        self.create_diagram()

    def create_first_follow(self):
        first_file = open('first.txt', 'r')
        first_Lines = first_file.readlines()
        firsts = []
        for line in first_Lines:
            firsts.append(line)

        follow_file = open('follow.txt', 'r')
        follow_Lines = follow_file.readlines()
        follows = []
        for line in follow_Lines:
            follows.append(line)

        nonterminal_file = open('nonterminal.txt', 'r')
        nonterminal_Lines = nonterminal_file.readlines()
        nonterminals = []
        for line in nonterminal_Lines:
            nonterminals.append(line)

        counter = 0
        for unter in nonterminals:
            self.firsts[unter] = firsts[counter]
            self.follows[unter] = follows[counter]

    def create_diagram(self):
        grammer_file = open('grammer.txt', 'r')
        grammer_lines = grammer_file.readlines()
        for line in grammer_lines:
            sl = line.split('->')
            rights = sl[1].split('|')
            max_len = 0
            for g in rights:
                l = g.split()
                if len(l) > max_len:
                    max_len = len(l)
            # max_len -=1
            states = dict()
            zero = dict()
            counter = 0
            for g in rights:
                space_split = g.split()
                if len(space_split) == 1:
                    zero[space_split[0]] = max_len
                else:
                    counter += 1
                    zero[space_split[0]] = counter
                    for t in space_split[1:len(space_split) - 1]:
                        h = dict()
                        h[t] = counter + 1
                        states[counter] = h
                        counter += 1
                    f = dict()
                    f[space_split[len(space_split) - 1]] = max_len
                    states[counter] = f
            states[0] = zero
            diagram = Diagram(sl[0], states)
            Diagram.all.append(diagram)
