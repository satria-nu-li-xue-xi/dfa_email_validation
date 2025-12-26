from typing import Dict, Set, Tuple, Optional, Callable

class DFA:
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transition: Dict[Tuple[str, str], str],
        start_state: str,
        accept_states: Set[str],
        on_step: Optional[Callable[[str, Optional[str], str], None]] = None,
    ):
        """
        states: himpunan state
        alphabet: himpunan simbol (karakter)
        transition: peta (state, simbol) -> next_state
        start_state: state awal
        accept_states: himpunan state penerima
        on_step: callback opsional untuk tracing (current_state, symbol, next_state)
        """
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states
        self.on_step = on_step

    def run(self, s: str) -> bool:
        state = self.start_state
        for ch in s:
            if (state, ch) not in self.transition:
                # Jika simbol tidak ada di alfabet atau transisi tidak didefinisikan: reject
                state = "qReject"
            else:
                next_state = self.transition[(state, ch)]
                if self.on_step:
                    self.on_step(state, ch, next_state)
                state = next_state
            if state == "qReject":
                if self.on_step:
                    self.on_step(state, None, state)
                return False
        return state in self.accept_states 