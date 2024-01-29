from collections.abc import Callable
from dataclasses import dataclass
from .NFA import NFA
from .Regex import Regex, parse_regex
from .DFA import DFA
import re


class Lexer:
    dfa_list = []
    Dfa = DFA(set(), set(), object(), {}, set())

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        
        nfa_list = []
        self.dfa_list = []
        
        for token, regex in spec:
            nfa_list.append((token, parse_regex(regex).thompson()))

        for i in nfa_list:
            self.dfa_list.append((i[0], i[1].subset_construction()))

        s = set()
        k = set()
        F = set()
        d = {}
        q0 = object()
        ok = 0
        for i in nfa_list:
            s = s.union(i[1].S)
            k.update(i[1].K)
            F.update(i[1].F)

            if ok == 0:
                d[(q0, "")] = set()
                d[(q0, "")].add(i[1].q0)
                ok = 1
            else:
                d[(q0, "")].add(i[1].q0)
                
            d.update(i[1].d)
    
        k.update({q0})
        s.add("")
        Nfa = NFA(s, k, q0, d, F)
        self.Dfa = Nfa.subset_construction()

    def check_sink(self, dfa, word):
        current_state = dfa.q0        
        for i in range(len(word)):
            if (current_state, word[i]) not in dfa.d:
                return i
            current_state = dfa.d.get(current_state,word[i])
            if current_state == frozenset():
                return i
        return len(word)

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        def accept_word(dfa_list, word):
            for token, dfa in dfa_list:
                if dfa.accept(word):
                    return token, word
            return None, None

        def get_error_message(index, word, num):
            nr_lines = len([char for char in copy[:index] if char == "\n"])
            last_pos = word.rfind("\n", 0, index) + 1

            if index + num >= len(word):
                return "No viable alternative at character EOF, line " + str(nr_lines)
            else:
                return ("No viable alternative at character "+ str(index + num - last_pos)+ ", line "+ str(nr_lines))

        res = []
        #st -> 1
        start = 1
        curent = ""
        copy = word
        index = 0

        while start <= len(word):
            if self.Dfa.accept(word[:start]):
                curent = word[:start]
            if start == len(word):
                if curent:
                    token, curent = accept_word(self.dfa_list, curent)
                    if token and curent:
                        res.append((token, curent))
                        word = word[len(curent) :]
                        index += len(curent)
                        curent = ""
                        start = 1
                else:
                    num = self.check_sink(self.Dfa, word)
                    return [("", get_error_message(index, copy, num))]
            else:
                start += 1
        return res
