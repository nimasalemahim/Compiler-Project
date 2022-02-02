class Rows:
    def __init__(self, lexeme, address, type_val):
        self.lexeme = lexeme
        self.address = address
        self.type_val = type_val


class SymbolTable:
    def __init__(self):
        self.rows = []
        self.pointer_address = 500
        self.scope_s = []

