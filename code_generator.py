class CodeGenerator:
    def __init__(self):
        self.semantic_stack = []

    def generate_code(self, action):
        getattr(self, action, )()

    def pid(self, a):
        print(a)
