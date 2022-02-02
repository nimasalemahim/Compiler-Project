class Rows:
    def __init__(self, lexeme, address, type_val, scope):
        self.lexeme = lexeme
        self.address = address
        self.type_val = type_val
        self.scope = scope
        self.num_array = 0


class SymbolTable:
    def __init__(self):
        self.rows = [Rows('a', 500, 'int', 1)]
        self.pointer_address = 500
        self.scope_s = []

    def insert(self, lexeme, type_val, scope):
        self.rows.append(Rows(lexeme, self.pointer_address, type_val, scope))
        self.pointer_address += 4


