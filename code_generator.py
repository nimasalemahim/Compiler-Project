from symbol_tabe import SymbolTable, Func, Param


class CodeGenerator:
    def __init__(self, symbol_table):
        self.semantic_stack = []
        self.scope = 0
        self.declaration_type = None
        self.latest_lexeme = None
        self.code_line = 1
        self.codes = {}
        self.symbol_table: SymbolTable = symbol_table
        self.operands = []
        self.declaration_id = False
        self.repeat_stack = []
        self.break_list = []
        self.last_func = None

    def generate_code(self, action, token):
        getattr(self, action, )(token)

    def fun_dec(self, *args):
        self.last_func = self.latest_lexeme
        Func(self.latest_lexeme)

    def params(self, token):
        address = self.symbol_table.get_free_address()
        self.symbol_table.insert(token, self.declaration_type, self.scope, address, True)
        self.latest_lexeme = token
        func = Func.get_name(self.last_func)
        func.params.append(Param(address, token))

    def array_param(self):
        func = Func.get_name(self.last_func)
        func.set_param_array(self.latest_lexeme)

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
        self.semantic_stack.append(f'#{num}')

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

    def rep_begin(self, *args):
        self.repeat_stack.append(self.code_line)

    def rep_end(self, *args):
        repeat = self.repeat_stack.pop()
        for break_line, repeat_line in self.break_list:
            if repeat == repeat_line:
                self.codes[break_line] = f'(JP, {self.code_line}, , )'

    def break_seen(self, *args):
        repeat = self.repeat_stack[-1]
        self.break_list.append((self.code_line, repeat))
        self.code_line += 1

    def jpf_save(self, *args):
        loc = self.semantic_stack.pop()
        result = self.semantic_stack.pop()

        self.codes[loc] = f'(JPF, {result}, {self.code_line + 1}, )'
        self.semantic_stack.append(self.code_line)
        self.code_line += 1

    def jp(self, *args):
        loc = self.semantic_stack.pop()
        self.codes[loc] = f'(JP, {self.code_line}, , )'

    def jpf(self, *args):
        loc = self.semantic_stack.pop()
        result = self.semantic_stack.pop()
        self.codes[loc] = f'(JPF, {result}, {self.code_line}, )'

    def save_rep(self, *args):
        self.semantic_stack.append(self.code_line)

    def jpf_rep(self, *args):
        result = self.semantic_stack.pop()
        loc = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(JPF, {result}, {loc}, )'
        self.code_line += 1

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
        self.codes[self.code_line] = f'({op_name}, {first}, {second}, {address})'
        self.code_line += 1

    def assign(self, *args):
        second = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(ASSIGN, {second}, {first}, )'
        self.code_line += 1

    def array_addr(self, *args):
        address = self.symbol_table.get_free_address()
        index = self.semantic_stack.pop()
        array_address = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(MULT, #4, {index}, {address})'
        self.code_line += 1
        self.codes[self.code_line] = f'(ADD, #{array_address}, {address}, {address})'
        self.semantic_stack.append(f"@{address}")
        self.code_line += 1
