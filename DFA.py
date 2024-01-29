from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]


    # method to check if a word is accepted by the DFA
    def accept(self, word: str) -> bool:
        current_state = self.q0
        
        for symbol in word:
            current_state = self.d.get((current_state, symbol))
            if current_state is None:
                return False

        return current_state in self.F

    


