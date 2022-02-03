from symbol_tabe import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table):
        self.semantic_stack = []
        self.scope = 0
        self.declaration_type = None
        self.latest_lexeme = None
        self.code_line = 0
        self.codes = {}
        self.symbol_table: SymbolTable = symbol_table
        self.operands = []
        self.declaration_id = False

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

    def pid_get(self, lexeme):
        row = self.symbol_table.get_row_by_lexeme(lexeme, self.scope)
        self.semantic_stack.append(row.address)

    def push_num(self, num):
        self.semantic_stack.append((num, "num"))

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

    def saveop(self, operand):
        self.operands.append(operand)

    def op(self, *args):
        second = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        operand = self.operands.pop()
        op_name = ""
        if operand == "+":
            op_name = "ADD"
        if operand == "-":
            op_name = "SUB"
        if operand == "*":
            op_name = "MULT"
        if operand == "<":
            op_name = "LT"
        if operand == "==":
            op_name = "EQ"
        address = self.symbol_table.get_free_address()
        self.semantic_stack.append(address)
        first_op, second_op = self.find_operation(first, second)
        self.codes[self.code_line] = f'({op_name}, {first_op}, {second_op}, {address})'
        self.code_line += 1

    def assign(self):
        second = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        first_op, second_op = self.find_operation(first, second)
        self.codes[self.code_line] = f'(ASSIGN, {first_op}, {second_op}, )'
        self.code_line += 1

    def find_operation(self, first, second):
        first_op = ""
        second_op = ""
        if type(first) is tuple:
            first_op = f'#{first[0]}'
        else:
            first_op = first
        if type(second) is tuple:
            second_op = f'#{second[0]}'
        else:
            second_op = second

        return first_op, second_op

