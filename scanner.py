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

    @property
    def in_comment(self):
        return self.in_line_comment or self.in_full_comment

    def process_on_new_char(self, char):
        if char is '\n':
            self.row_counter += 1
        end = False
        while not end:
            self.string = f'{self.string}{char}'
            char_type = get_type(char)

            if char_type is ILLEGAL_TYPE and not self.in_full_comment:
                self.lexical_errors.get(self.row_counter, []).append(f"({self.string}, {INVALID_INPUT}) ")
                self.dfa.set_state_by_id(0)
                self.string = ""

            elif self.dfa.state.have_other and self.dfa.state.char_type_is_illegal_other(char_type):
                if char_type in WHITE_SPACES:
                    self.string = f'{self.string[0:-1]}'
                self.lexical_errors.get(self.row_counter, []).append(
                    f"({self.string}, {self.dfa.state.error_message}) ")

            elif self.dfa.state.have_transition_state_with_type(char_type):
                self.dfa.set_state(self.dfa.state.get_transition_state(char_type))

    def get_next_token(self):
        if self.found_tokens:
            return self.found_tokens.pop(0)
        while not self.found_tokens:
            char = self.input_file.read(1)
            if char is '':
                return '', 'END'
            self.process_on_new_char(char)
        return self.found_tokens.pop(0)
