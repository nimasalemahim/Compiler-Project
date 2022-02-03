from symbol_tabe import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table):
        self.semantic_stack = []
        self.operand = None
        self.scope = 0
        self.declaration_type = None
        self.latest_lexeme = None
        self.code_line = 0
        self.codes = {}
        self.symbol_table: SymbolTable = symbol_table
        # self.latest_op = []

    def generate_code(self, action, token):
        print(action)
        getattr(self, action, )(token)

    def pid(self, lexeme):
        self.latest_lexeme = lexeme
        address = self.symbol_table.get_free_address()
        self.symbol_table.insert(lexeme, self.declaration_type, self.scope, address)
        code = f'(ASSIGN, #0, {address}, )'
        self.codes[self.code_line] = code
        self.code_line += 1

    def array(self, num):
        row = self.symbol_table.get_row_by_lexeme(self.latest_lexeme, self.scope)
        row.num_array = int(num)
        for _ in range(int(num) - 1):
            code = f'(ASSIGN, #0, {self.symbol_table.get_free_address()}, )'
            self.codes[self.code_line] = code
            self.code_line += 1

    def type_save(self, val_type):
        self.declaration_type = val_type

    def scope_increase(self, *args):
        self.scope += 1

    def scope_decrease(self, *args):
        self.symbol_table.delete_in_scope(self.scope)
        self.scope -= 1

    def save(self, *args):
        self.semantic_stack.append(self.code_line)
        self.code_line += 1

    def jpf_save(self, *args):
        # try:
        loc = self.semantic_stack.pop()
        result = self.semantic_stack.pop()
        self.codes[loc] = f'(JPF, {result}, {self.code_line + 1}, )'
        self.semantic_stack.append(self.code_line)
        self.code_line += 1
        # except:
        #     pass

    def jp(self, *args):
        # try:
        loc = self.semantic_stack.pop()
        self.codes[loc] = f'(JP, {self.code_line}, , )'
        # except:
        #     pass

    def jpf(self, *args):
        # try:
        loc = self.semantic_stack.pop()
        result = self.semantic_stack.pop()
        self.codes[loc] = f'(JPF, {result}, {self.code_line}, )'
        # except:
        #     pass

    def save_rep(self, *args):
        self.semantic_stack.append(self.code_line)

    def jpf_rep(self, *args):
        # try:
        result = self.semantic_stack.pop()
        loc = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(JPF, {result}, {loc}, )'
        self.code_line += 1
        # except:
        #     pass

    # def opp(self):
    #     print('op')
    #
    # def ASA(self):
    #     print('ASA')
