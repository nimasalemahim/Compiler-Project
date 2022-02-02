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

    def generate_code(self, action, token):
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

    def type_save(self, type):
        self.declaration_type = type

    # def opp(self):
    #     print('op')
    #
    # def ASA(self):
    #     print('ASA')
