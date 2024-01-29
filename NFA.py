from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]
    
    

    #method which returns the epsilon closure of a state
    def epsilon_closure(self, state: STATE) -> set[STATE]:
        closure = set([state])
        states_to_process = [state]

        while states_to_process:
            current_state = states_to_process.pop()
            next_states = self.d.get((current_state, EPSILON), [])   
            
            for next_state in next_states:
                if next_state not in closure:
                    closure.add(next_state)
                    states_to_process.append(next_state)
        
        return closure

    
    #method which returns the DFA obtained from the subset construction algorithm
    def subset_construction(self) -> DFA[frozenset[STATE]]:
        
        start_state = frozenset(self.epsilon_closure(self.q0))
        dfa_transitions = {}
        dfa_states = set()
        dfa_states.add(frozenset(self.epsilon_closure(self.q0)))
        dfa_final_states = set()
        
        states_to_process = [frozenset(self.epsilon_closure(self.q0))]
        while states_to_process:
            current_state = states_to_process.pop()
            for symbol in self.S:
                next_states = set()
                for state in current_state:
                    if (state,symbol) in self.d:
                        next_states.update (self.d.get ( (state,symbol),[]))
                next_states = {i for s in next_states for i in self.epsilon_closure(s)} 
                if frozenset (next_states):
                    dfa_transitions [(frozenset(current_state),symbol)] = frozenset(next_states)
                    if frozenset(next_states) not in dfa_states:
                        dfa_states.add(frozenset(next_states))
                        states_to_process.append(frozenset(next_states))
        
        l = [i for i in dfa_states if i.intersection(self.F)]
        dfa_final_states = set(l)  
        dfa_states.add(frozenset())
        for i in self.S:
            for state1 in dfa_states:
                if (state1,i) not in dfa_transitions:
                    dfa_transitions[(state1,i)]=frozenset()
        
        return DFA(self.S,dfa_states,start_state,dfa_transitions,dfa_final_states)
        
        
 
