from utils import *


class Scanner:
    def __init__(self, input_file, dfa):
        self.dfa = dfa
        self.input_file = input_file
        self.symbols_arr = KEYWORDS.copy()
        self.row_counter = 1
        self.lexical_errors = {}
        self.tokens = {}
        self.found_tokens = []
        self.dfa.set_state_by_id(0)
        self.string = ""
        self.in_line_comment = False
        self.in_full_comment = False
        self.comment_line = None

    @property
    def in_comment(self):
        return self.in_line_comment or self.in_full_comment

    def is_in_symbols_arr(self, string):
        return string in self.symbols_arr

    def process_on_new_char(self, char):
        if char == '\n':
            self.row_counter += 1
        end = False
        while not end:
            end = True
            self.string = f'{self.string}{char}'
            char_type = get_type(char)

            if char_type is ILLEGAL_TYPE and not self.in_comment:
                error = f"({self.string}, {INVALID_INPUT}) "
                self.add_to_lexical_errors(error)
                self.dfa.set_state_by_id(0)
                self.string = ""

            elif self.dfa.state.have_other and self.dfa.state.char_type_is_illegal_other(char_type):
                if char_type in WHITE_SPACES:
                    self.string = f'{self.string[0:-1]}'
                error = f"({self.string}, {self.dfa.state.error_message}) "
                self.add_to_lexical_errors(error)
                self.dfa.set_state_by_id(0)
                self.string = ""

            elif self.dfa.state.have_transition_state_with_type(char_type):
                self.dfa.set_state(self.dfa.state.get_transition_state(char_type))
            else:
                if not self.dfa.state.have_other:
                    row_num = self.row_counter
                    if self.dfa.state.id == 10:
                        self.string = f'{self.string[0:-1]}'
                        if char_type == '\n':
                            row_num -= 1
                        end = False
                    error = f"({self.string}, {self.dfa.state.error_message}) "
                    self.add_to_lexical_errors(error, row_num)
                    self.dfa.set_state_by_id(0)
                    self.string = ''
                else:
                    if self.dfa.state.get_transition_state(OTHER_TYPE):
                        self.dfa.set_state(self.dfa.state.get_transition_state(OTHER_TYPE))
                    else:
                        self.dfa.set_state_by_id(0)

            if self.dfa.state.id == 11 or self.dfa.state.id == 13:
                if not self.in_comment:
                    self.comment_line = self.row_counter
                if self.dfa.state.id == 11:
                    self.in_line_comment = True
                else:
                    self.in_full_comment = True

            if self.dfa.state.is_final:
                row_num = self.row_counter
                if self.dfa.state.have_star:
                    self.string = f'{self.string[0: -1]}'
                    if char_type == '\n':
                        row_num -= 1
                    end = False

                if self.dfa.state.id == 2:
                    if not is_in_keyword(self.string):
                        if not self.is_in_symbols_arr(self.string):
                            self.symbols_arr.append(self.string)
                        self.add_to_found_tokens((ID, self.string), row_num)
                    else:
                        self.add_to_found_tokens((KEYWORD, self.string), row_num)

                elif self.dfa.state.id == 4:
                    self.add_to_found_tokens((NUM, self.string), row_num)

                elif self.dfa.state.id == 5 or self.dfa.state.id == 7 or self.dfa.state.id == 9:
                    self.add_to_found_tokens((SYMBOL, self.string), row_num)

                elif self.dfa.state.id == 12:
                    self.in_full_comment = False
                    self.in_line_comment = False

                self.string = ''
                self.dfa.set_state_by_id(0)

    def add_to_lexical_errors(self, error, row_num=None):
        if not row_num:
            row_num = self.row_counter
        row = self.lexical_errors.get(row_num, [])
        row.append(error)
        self.lexical_errors[row_num] = row

    def add_to_found_tokens(self, token, row_num=None):
        if not row_num:
            row_num = self.row_counter
        self.found_tokens.append(token)
        row = self.tokens.get(row_num, [])
        row.append(token)
        self.tokens[row_num] = row

    def get_next_token(self):
        if self.found_tokens:
            return self.found_tokens.pop(0)
        end_file = False
        while not self.found_tokens:
            if end_file:
                return '', END
            char = self.input_file.read(1)
            if char == '':
                if self.in_comment:
                    error = f"({self.string[:7]}..., {UNCLOSED_COMMENT}) "
                    self.add_to_lexical_errors(error, self.comment_line)
                end_file = True
                char = '\n'
            self.process_on_new_char(char)
        return self.found_tokens.pop(0)

    def write_tokens(self, file_name):
        with open(file_name, 'w') as f:
            for row in self.tokens.keys():
                f.write(str(row) + '.\t')
                f.write(' '.join(f'({token_type}, {string})' for token_type, string in self.tokens[row]))
                f.write('\n')

    def write_symbol_table(self, file_name):
        with open(file_name, 'w') as ST:
            for index, sym in enumerate(self.symbols_arr):
                ST.write(str(index + 1) + ".\t" + sym + '\n')

    def write_lexical_errors(self, file_name):
        with open(file_name, 'w') as f:
            if not self.lexical_errors.keys():
                f.write("There is no lexical error.")
            for row in self.lexical_errors.keys():
                f.write(str(row) + ".\t")
                f.write(' '.join(s[0: -1] for s in self.lexical_errors[row]))
                f.write('\n')

    def write_files(self):
        self.write_symbol_table('symbol_table.txt')
        self.write_lexical_errors('lexical_errors.txt')
        self.write_tokens('tokens.txt')
