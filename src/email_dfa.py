import string
from .dfa import DFA

# Definisi alfabet
USERNAME_CHARS = set(string.ascii_letters + string.digits + "._")
DOMAIN_CHARS = set(string.ascii_letters + string.digits)
EXTENSION_CHARS = set(string.ascii_letters)

class EmailDFAWithCounter:
    def __init__(self):
        self.ext_len = 0
        states = {"q0", "q1", "q2", "q3", "qReject"}
        alphabet = set(string.printable)
        transition = {}

        def add_trans(s, chars, t):
            for c in chars:
                transition[(s, c)] = t

        # q0 → q1
        add_trans("q0", USERNAME_CHARS, "q1")
        # q1
        add_trans("q1", USERNAME_CHARS, "q1")
        transition[("q1", "@")] = "q2"
        # q2
        add_trans("q2", DOMAIN_CHARS, "q2")
        transition[("q2", ".")] = "q3"
        # q3
        add_trans("q3", EXTENSION_CHARS, "q3")

        self.dfa = DFA(states, alphabet, transition, "q0", {"q3"})

    def validate(self, email: str) -> bool:
        self.ext_len = 0
        domain_len = 0
        state = "q0"
        for ch in email:
            if (state, ch) not in self.dfa.transition:
                return False
            next_state = self.dfa.transition[(state, ch)]
            if state == "q1" and ch == "@":
                domain_len = 0
            if state == "q2" and ch in DOMAIN_CHARS:
                domain_len += 1
            if state == "q2" and ch == "." and domain_len == 0:
                return False
            state = next_state
            if state == "q3" and ch in EXTENSION_CHARS:
                self.ext_len += 1
        return state == "q3" and self.ext_len >= 2


class EmailDFAExpandedStates:
    def __init__(self):
        states = {"q0", "q1", "q2", "q3a", "q3b", "qReject"}
        alphabet = set(string.printable)
        transition = {}

        def add_trans(s, chars, t):
            for c in chars:
                transition[(s, c)] = t

        # q0 → q1
        add_trans("q0", USERNAME_CHARS, "q1")
        # q1
        add_trans("q1", USERNAME_CHARS, "q1")
        transition[("q1", "@")] = "q2"
        # q2
        add_trans("q2", DOMAIN_CHARS, "q2")
        transition[("q2", ".")] = "q3a"
        # q3a (ext_len = 1)
        add_trans("q3a", EXTENSION_CHARS, "q3b")
        # q3b (ext_len ≥ 2)
        add_trans("q3b", EXTENSION_CHARS, "q3b")

        self.dfa = DFA(states, alphabet, transition, "q0", {"q3b"})

    def validate(self, email: str) -> bool:
        state = "q0"
        domain_len = 0
        ext_len = 0
        for ch in email:
            if (state, ch) not in self.dfa.transition:
                return False
            next_state = self.dfa.transition[(state, ch)]
            if state == "q1" and ch == "@":
                domain_len = 0
            if state == "q2" and ch in DOMAIN_CHARS:
                domain_len += 1
            if state == "q2" and ch == "." and domain_len == 0:
                return False
            if next_state in {"q3a", "q3b"} and ch in EXTENSION_CHARS:
                ext_len += 1
            state = next_state
        return state == "q3b" and ext_len >= 2
