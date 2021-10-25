import re

STATE_NUM = 16
ROW_NUM = 10000
LETTER_TYPE = 'letter'
DIGIT_TYPE = 'digit'
OTHER_TYPE = 'other'
ILLEGAL_TYPE = 'illegal'
KEYWORD = "KEYWORD"
ID = "ID"
NUM = "NUM"
SYMBOL = "SYMBOL"
NO_OTHER_SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<']
WHITE_SPACES = [' ', '\n', '\t', '\r', '\f', '\v']
VALID_SYMBOLS = NO_OTHER_SYMBOLS.copy() + ['=', '*', '/'] + WHITE_SPACES.copy()
KEYWORDS = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
INVALID_INPUT = 'Invalid input'


def get_type(char):
    if re.match(r'[a-zA-Z]', char):
        return LETTER_TYPE

    elif re.match(r'[0-9]', char):
        return DIGIT_TYPE

    elif char in self.valid_symbols:
        return char
    return ILLEGAL_TYPE
