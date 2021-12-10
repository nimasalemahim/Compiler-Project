# Nima Salem 			97106002
# Majid Taherkhani	97106108
from diagram import Diagram
from parse import Parser

from scanner import Scanner
from utils import *
from DFA import DFA
from parse import Parser


def create_dfa():
    dfa = DFA([i for i in range(STATE_NUM)])
    dfa.add_transition_to_state(source_id=0, situation=LETTER_TYPE, final_id=1)
    dfa.add_transition_to_state(source_id=0, situation=DIGIT_TYPE, final_id=3)
    for sym in NO_OTHER_SYMBOLS:
        dfa.add_transition_to_state(source_id=0, situation=sym, final_id=5)
    dfa.add_transition_to_state(source_id=0, situation="=", final_id=6)
    dfa.add_transition_to_state(source_id=0, situation="*", final_id=8)
    dfa.add_transition_to_state(source_id=0, situation="/", final_id=10)
    for ws in WHITE_SPACES:
        dfa.add_transition_to_state(source_id=0, situation=ws, final_id=15)
    dfa.change_state_have_other(0, False)
    dfa.set_state_error_message(0, INVALID_INPUT)

    dfa.add_transition_to_state(source_id=1, situation=LETTER_TYPE, final_id=1)
    dfa.add_transition_to_state(source_id=1, situation=DIGIT_TYPE, final_id=1)
    dfa.add_transition_to_state(source_id=1, situation=OTHER_TYPE, final_id=2)

    dfa.make_state_final(2)
    dfa.make_state_have_star(2)

    dfa.add_transition_to_state(source_id=3, situation=DIGIT_TYPE, final_id=3)
    dfa.add_state_no_other_chars(3, [LETTER_TYPE])
    dfa.add_transition_to_state(source_id=3, situation=OTHER_TYPE, final_id=4)
    dfa.set_state_error_message(3, INVALID_NUMBER)

    dfa.make_state_final(4)
    dfa.make_state_have_star(4)

    dfa.make_state_final(5)

    dfa.add_transition_to_state(source_id=6, situation='=', final_id=7)
    dfa.add_transition_to_state(source_id=6, situation=OTHER_TYPE, final_id=9)

    dfa.make_state_final(7)

    dfa.add_state_no_other_chars(8, ["/"])
    dfa.add_transition_to_state(source_id=8, situation=OTHER_TYPE, final_id=9)
    dfa.set_state_error_message(8, UNMATCHED_COMMENT)

    dfa.make_state_final(9)
    dfa.make_state_have_star(9)

    dfa.add_transition_to_state(source_id=10, situation="/", final_id=11)
    dfa.add_transition_to_state(source_id=10, situation="*", final_id=13)
    dfa.change_state_have_other(10, False)
    dfa.set_state_error_message(10, INVALID_INPUT)

    dfa.add_transition_to_state(source_id=11, situation="\n", final_id=12)
    dfa.add_transition_to_state(source_id=11, situation=OTHER_TYPE, final_id=11)

    dfa.make_state_final(12)

    dfa.add_transition_to_state(source_id=13, situation="*", final_id=14)
    dfa.add_transition_to_state(source_id=13, situation=OTHER_TYPE, final_id=13)

    dfa.add_transition_to_state(source_id=14, situation="/", final_id=12)
    dfa.add_transition_to_state(source_id=14, situation="*", final_id=14)
    dfa.add_transition_to_state(source_id=14, situation=OTHER_TYPE, final_id=13)

    dfa.make_state_final(15)

    return dfa


if __name__ == '__main__':
    dfa = create_dfa()
    input_file = open('input.txt', 'r')
    scanner = Scanner(input_file, dfa=dfa)
    parser = Parser(scanner)
    parser.start()
    parser.save_tree('parse_tree.txt')
    parser.save_errors('syntax_errors.txt')

    # while True:
    #     k = scanner.get_next_token()
    #     print(k)
    #     r, (p1, p2) = k
    #     if p1 == END:
    #         break

    scanner.write_files()

    input_file.close()
