class Rows:
    def __init__(self, lexeme, address, type_val, scope):
        self.lexeme = lexeme
        self.address = address
        self.type_val = type_val
        self.scope = scope
        self.num_array = 0

    def __str__(self):
        return f'l: {self.lexeme}, a: {self.address}, t_v: {self.type_val}, s: {self.scope}, n_a: {self.num_array}'


class SymbolTable:
    def __init__(self):
        self.rows = []
        self.pointer_address = 496
        self.scope_s = []

    def insert(self, lexeme, type_val, scope, address):
        self.rows.append(Rows(lexeme, address, type_val, scope))

    def get_free_address(self):
        self.pointer_address += 4
        return self.pointer_address

    def get_row_by_lexeme(self, lexeme, scope):
        for row in self.rows:
            if row.scope == scope and row.lexeme == lexeme:
                return row

    def delete_in_scope(self, scope):
        for row in self.rows:
            if row.scope == scope:
                self.rows.remove(row)

    def __str__(self):
        string = ''
        for row in self.rows:
            string = f'{string}{str(row)}\n'
        return string
