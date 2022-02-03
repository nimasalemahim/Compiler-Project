class Func:
    all_func = []

    def __init__(self, name, type):
        self.name = name
        self.params = []
        self.address = 0
        self.code_line = 0
        self.type = type
        Func.all_func.append(self)

    def set_param_array(self, param_name):
        for param in self.params:
            if param.name == param_name:
                param.isarray = True
                return

    @staticmethod
    def get_name(name):
        for i in Func.all_func:
            if i.name == name:
                return i


class Param:
    def __init__(self, address, name):
        self.name = name
        self.address = address
        self.isarray = False


class Rows:
    def __init__(self, lexeme, address, type_val, scope, isparam=False):
        self.lexeme = lexeme
        self.address = address
        self.type_val = type_val
        self.scope = scope
        self.num_array = 0
        self.isparam = isparam

    def __str__(self):
        return f'l: {self.lexeme}, a: {self.address}, t_v: {self.type_val}, s: {self.scope}, n_a: {self.num_array}'


class SymbolTable:
    def __init__(self):
        self.rows = []
        self.pointer_address = 496
        self.scope_s = []

    def insert(self, lexeme, type_val, scope, address, isparam=False):
        self.rows.append(Rows(lexeme, address, type_val, scope, isparam))

    def get_free_address(self):
        self.pointer_address += 4
        return self.pointer_address

    def get_row_by_lexeme(self, lexeme, scope):
        for scope in list(reversed(range(scope + 1))):
            for row in self.rows:
                if row.scope == scope and row.lexeme == lexeme:
                    return row

    def delete_in_scope(self, scope):
        self.rows = list(filter(lambda x: x.scope != scope < 5, self.rows))

    def __str__(self):
        string = ''
        for row in self.rows:
            string = f'{string}{str(row)}\n'
        return string