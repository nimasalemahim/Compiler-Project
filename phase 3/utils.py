import re

DEBUG = False
STATE_NUM = 16
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
KEYWORDS = ["if", "else", "void", "int", "repeat", "break", "until", "return", 'endif']
INVALID_INPUT = 'Invalid input'
END = 'END'
UNCLOSED_COMMENT = 'Unclosed comment'
INVALID_NUMBER = "Invalid number"
UNMATCHED_COMMENT = "Unmatched comment"

if DEBUG:
    START_STATE = 'K'
else:
    START_STATE = 'Program'

EPSILON = 'EPSILON'
EPSILON_tree = 'epsilon'


def get_type(char):
    if re.match(r'[a-zA-Z]', char):
        return LETTER_TYPE

    elif re.match(r'[0-9]', char):
        return DIGIT_TYPE

    elif char in VALID_SYMBOLS:
        return char
    return ILLEGAL_TYPE


def is_in_keyword(string):
    return string in KEYWORDS
