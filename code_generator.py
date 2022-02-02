class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []
        self.operand = None
        self.scope = 0
        self.declaration_type = None
        self.latest_lexeme = None

    def generate_code(self, action):
        getattr(self, action, )()

    def pid(self):
        print('pid')

    def pid2(self):
        print('pid2')

    def assign(self):
        print('assign')

    def opp(self):
        print('op')

    def ASA(self):
        print('ASA')
