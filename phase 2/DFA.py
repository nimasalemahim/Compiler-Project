class State:
    def __init__(self, id):
        self.id = id
        self.is_final = False
        self.have_star = False
        self.have_other = True
        self.no_other_chars = []
        self.error_message = ""
        self.transition_states = {}

    def have_transition_state_with_type(self, char_type):
        return char_type in self.transition_states

    def char_type_is_illegal_other(self, char_type):
        return char_type in self.no_other_chars

    def get_transition_state(self, char_type):
        return self.transition_states.get(char_type, None)


class DFA:

    def __init__(self, state_ids: list):
        self.all_states = []
        self.state = None
        for id in state_ids:
            self.all_states.append(State(id=id))

    def __get_state_by_id(self, id):
        for state in self.all_states:
            if state.id == id:
                return state
        return None

    def make_state_final(self, id):
        state = self.__get_state_by_id(id)
        state.is_final = True

    def make_state_have_star(self, id):
        state = self.__get_state_by_id(id)
        state.have_star = True

    def change_state_have_other(self, id, bol):
        state = self.__get_state_by_id(id)
        state.have_other = bol

    def set_state_error_message(self, id, message):
        state = self.__get_state_by_id(id)
        state.error_message = message

    def add_state_no_other_chars(self, id, no_other_chars: list):
        state = self.__get_state_by_id(id)
        state.no_other_chars = state.no_other_chars + no_other_chars

    def add_transition_to_state(self, source_id, situation, final_id):
        source_state = self.__get_state_by_id(source_id)
        final_state = self.__get_state_by_id(final_id)
        source_state.transition_states[situation] = final_state

    def set_state_by_id(self, id):
        self.state = self.__get_state_by_id(id)

    def set_state(self, state: State):
        self.state = state
