class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []
        self.operand = None

    def generate_code(self, action):
        getattr(self, action, )()

    def pid(self):
        print('pid')

    def assign(self):
        print('assign')

    def opp(self):
        print('op')

    def ASA(self):
        print('ASA')
