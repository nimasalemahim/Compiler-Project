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
        self.in_param_initial = False
        self.func_params = []
        self.calling_func = None
        self.return_stack = []

    def generate_code(self, action, token):
        getattr(self, action, )(token)

    def fun_dec(self, *args):
        self.last_func = self.latest_lexeme
        return_address = self.symbol_table.get_free_address()
        func = Func(self.latest_lexeme, self.declaration_type, return_address)
        func.code_line = self.code_line - 1
        # print(self.semantic_stack)
        # self.semantic_stack.pop()

    def param_init(self, *args):
        self.in_param_initial = True

    def param_exit(self, *args):
        self.in_param_initial = False

    def array_param(self, *args):
        func = Func.get_name(self.last_func)
        func.set_param_array(self.latest_lexeme)

    def pid(self, lexeme):
        self.latest_lexeme = lexeme
        address = self.symbol_table.get_free_address()
        if self.in_param_initial:
            func = Func.get_name(self.last_func)
            func.params.append(Param(address, lexeme))
            address = f'@{address}'
        else:
            code = f'(ASSIGN, #0, {address}, )'
            self.codes[self.code_line] = code
            self.code_line += 1
        self.symbol_table.insert(lexeme, self.declaration_type, self.scope, address)

    def pid_get(self, lexeme):
        self.latest_lexeme = lexeme
        row = self.symbol_table.get_row_by_lexeme(lexeme, self.scope)
        if not Func.is_exists(lexeme):
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
        print(second, first)
        self.codes[self.code_line] = f'(ASSIGN, {second}, {first}, )'
        self.code_line += 1

    def array_addr(self, *args):
        address = self.symbol_table.get_free_address()
        index = self.semantic_stack.pop()
        array_address = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(MULT, #4, {index}, {address})'
        self.code_line += 1
        if '@' in str(array_address):
            self.codes[self.code_line] = f'(ADD, {array_address.replace("@", "")}, {address}, {address})'
        else:
            self.codes[self.code_line] = f'(ADD, #{array_address}, {address}, {address})'
        self.semantic_stack.append(f"@{address}")
        self.code_line += 1

    def call_start(self, *args):
        func = Func.get_name(self.latest_lexeme)
        self.calling_func = func
        self.func_params = func.params.copy()

    def set_arg(self, *args):
        semantic = self.semantic_stack.pop()
        if '#' in str(semantic):
            temp = self.symbol_table.get_free_address()
            self.codes[self.code_line] = f'(ASSIGN, {semantic}, {temp}, )'
            self.code_line += 1
            arg = self.func_params.pop(0)
            arg_address = arg.address
            self.codes[self.code_line] = f'(ASSIGN, #{temp}, {arg_address}, )'
            self.code_line += 1
        else:
            arg = self.func_params.pop(0)
            arg_address = arg.address
            self.codes[self.code_line] = f'(ASSIGN, #{semantic}, {arg_address}, )'
            self.code_line += 1

    def set_return_val(self, *args):
        semantic = self.semantic_stack.pop()
        self.codes[self.code_line] = f'(ASSIGN, {semantic}, 1500, )'
        self.code_line += 1

    def return_line(self, *args):
        func = Func.get_name(self.last_func)
        address = func.return_address
        self.codes[self.code_line] = f'(JP, @{address}, , )'
        self.code_line += 1

    def call_end(self, *args):
        func_line = self.calling_func.code_line
        self.codes[self.code_line] = f'(ASSIGN, #{self.code_line + 2}, {self.calling_func.return_address}, )'
        self.code_line += 1
        self.codes[self.code_line] = f'(JP, {func_line}, , )'
        self.code_line += 1
        if self.calling_func.type == 'int':
            address = self.symbol_table.get_free_address()
            self.codes[self.code_line] = f'(ASSIGN, 1500, {address}, )'
            self.code_line += 1
            print(self.semantic_stack)
            self.semantic_stack.append(address)


