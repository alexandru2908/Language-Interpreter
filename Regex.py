from .NFA import NFA
# from Operations import Star, Plus, Intrebare, Concatenare, Pipe, Char


class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')    

# add the necessary transitions and states to complete the NFA
class Star(Regex):
    def thompson(self) -> NFA[int]:
        nfa_preceding = self.valoare.thompson()
        start_state = object()
        accept_state = object()

        transitions = nfa_preceding.d.copy()
        transitions[(start_state, '')] = {nfa_preceding.q0, accept_state}
        
        for state in nfa_preceding.F:
            transitions[(state, '')] = {accept_state, nfa_preceding.q0}

        return NFA(nfa_preceding.S ,
                   nfa_preceding.K | {start_state, accept_state},
                   start_state,
                   transitions,
                   {accept_state})
    name="Star"  
    def __init__(self, regex):
        self.valoare = regex
        
# add the necessary transitions and states to complete the NFA        
class Plus(Regex):
    def thompson(self) -> NFA[int]:
        nfa_preceding = self.valoare.thompson()
        #star,acept object      
        start_state = object()
        accept_state = object()

        transitions = nfa_preceding.d.copy()
        #tranz pe eps de la start la q0
        transitions[(start_state, '')] = {nfa_preceding.q0}
        for state in nfa_preceding.F:
        #parc F si adaug eps tranz la q0, accept
            transitions[(state, '')] = {accept_state,nfa_preceding.q0}

        return NFA(nfa_preceding.S | {''},
                   nfa_preceding.K | {start_state, accept_state},
                   start_state,
                   transitions,
                   {accept_state})
    name="Plus"
    def __init__(self, regex):
        self.valoare = regex

# add the necessary transitions and states to complete the NFA
class Intrebare(Regex):
    def thompson(self) -> NFA[int]:
        nfa_preceding = self.valoare.thompson()
        start_state = object()
        accept_state = object()
        
        transitions = nfa_preceding.d.copy()
        transitions[(start_state, '')] = {nfa_preceding.q0, accept_state}\
            
        for state in nfa_preceding.F:
            transitions[(state, '')] = {accept_state}

        return NFA(nfa_preceding.S | {''},
                   nfa_preceding.K | {start_state, accept_state},
                   start_state,
                   transitions,
                   {accept_state})
    name="Intrebare"
    def __init__(self, regex):
        self.valoare = regex

# add the necessary transitions and states to complete the NFA
class Concatenare(Regex):
    def thompson(self) -> NFA[int]:
        nfa_preceding = self.valoare1.thompson()
        nfa_next = self.valoare2.thompson()
        start_state = nfa_preceding.q0
        accept_state = nfa_next.F

        transitions = nfa_preceding.d.copy()
        transitions.update(nfa_next.d)

        for state in nfa_preceding.F:
            transitions[(state, '')] = {nfa_next.q0}

        return NFA(nfa_preceding.S | nfa_next.S,
                   nfa_preceding.K | nfa_next.K | {start_state} | accept_state,
                   start_state,
                   transitions,
                   accept_state)
    name="Concatenare"
    def __init__(self, regex1, regex2):
        self.valoare1 = regex1
        self.valoare2 = regex2

# add the necessary transitions and states to complete the NFA
class Pipe(Regex):
    def thompson(self) -> NFA[int]:
        nfa_preceding = self.valoare1.thompson()
        nfa_next = self.valoare2.thompson()
        start_state = object()
        accept_state = object()

        transitions = {}
        transitions.update(nfa_preceding.d)
        transitions.update(nfa_next.d)
        transitions[(start_state, '')] = {nfa_preceding.q0, nfa_next.q0}

        for state in nfa_preceding.F:
            transitions[(state, '')] = {accept_state}
        for state in nfa_next.F:
            transitions[(state, '')] = {accept_state}

        return NFA(nfa_preceding.S | nfa_next.S,
                   nfa_preceding.K | nfa_next.K | {start_state, accept_state},
                   start_state,
                   transitions,
                   {accept_state})
    name="Pipe"
    def __init__(self, regex1, regex2):
        self.valoare1 = regex1
        self.valoare2 = regex2
        
class Char(Regex):
    
    def __init__(self, value):
        self.valoare = value
        
    def thompson(self) -> NFA[int]:
        start_state = object()
        accept_state = object()
        return NFA({self.valoare, ''}, {start_state, accept_state}, start_state, {(start_state, self.valoare): {accept_state}}, {accept_state})
    name="Char"
    
    

# function to parse a regex into a Regex object
def parse_regex(regex: str) -> Regex:
    
    lChars = []
    LChars=[]
    #regex [a-z]
    i='a'
    while i<= 'z':
        lChars.append(Char(i))
        i=chr(ord(i)+1)
    az=Pipe(lChars[0],lChars[1])
    for i in range(2,len(lChars)):
        az=Pipe(az,lChars[i])
        
    #regex [A-Z]
    i='A'
    while i<= 'Z':
        LChars.append(Char(i))
        i=chr(ord(i)+1)
    AZ=Pipe(LChars[0],LChars[1])
    for i in range(2,len(LChars)):
        AZ=Pipe(AZ,LChars[i])
    
    #regex [0-9]
    lDigits = []
    i='0'
    while i<= '9':
        lDigits.append(Char(i))
        i=chr(ord(i)+1)
    zero_noua=Pipe(lDigits[0],lDigits[1])
    for i in range(2,len(lDigits)):
        zero_noua=Pipe(zero_noua,lDigits[i])
        
    
    ok = 0
    l = list(regex)
    regexAnterior = []
    ok_paranteza = 0
    ok_par_dreapta = 0 
    ultima_paranteza = 0
    skip=0
    for s in range(len(l)):
        if ok_paranteza == 1 and s <= ultima_paranteza:
            if s == ultima_paranteza:
                ok_paranteza = 0
            continue
        if skip == 1:
            skip = 0
            continue
        if l[s] == "[":
            l2 = []
            ok_par_dreapta = 1
            for s1 in range(s+1,len(l)):
                if l[s1] == "]":
                    break
                else:
                    l2.append(l[s1])
            if l2[0] == 'a':
                regexAnterior.append(az)
            elif l2[0] == 'A':
                regexAnterior.append(AZ)
            elif l2[0] == '0':
                regexAnterior.append(zero_noua)
        elif ok_par_dreapta == 1:
            if l[s] == "]":
                ok_par_dreapta = 0
        elif l[s] == ' ':
                continue
        elif l[s] in ['*', '+', '?']:
            if len(regexAnterior)>0:
                if l[s] == '*':
                    regexAnterior.append(Star(regexAnterior.pop() ))
                elif l[s] == '+':
                      regexAnterior.append(Plus(regexAnterior.pop()))
                elif l[s] == '?':
                    regexAnterior.append(Intrebare(regexAnterior.pop()))
        
        elif l[s] == '(':
            ok_paranteza = 1
            ct = s+1
            ok = 1
            while ok != 0 and ct < len(l):
                if l[ct] == "//":
                    ct = ct + 2
                elif l[ct] == "(":
                    ok = ok + 1
                else:
                    if l[ct] == ")":
                        ok = ok - 1
                ct = ct + 1 
            ultima_paranteza = ct - 1
            regexAnterior.append(parse_regex(regex[s + 1:ct - 1]))
        elif l[s] == '|':
            if len(regexAnterior) == 1:
                return Pipe(regexAnterior.pop(),parse_regex(regex[s + 1:]))
            else:
                nume = Concatenare(regexAnterior[0],regexAnterior[1])
                for i in range(2,len(regexAnterior)):
                    nume = Concatenare(nume,regexAnterior[i])
                return Pipe(nume,parse_regex(regex[s + 1:]))  
            #daca e \\      
        elif l[s] == '\\':
            regexAnterior.append(Char(l[s + 1]))
            skip=1
        else:
            regexAnterior.append(Char(l[s]))
    for i in range(1,len(regexAnterior)):
        regexAnterior[0]=Concatenare(regexAnterior[0],regexAnterior[i])
    return regexAnterior[0]



            
            