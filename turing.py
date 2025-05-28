from dataclasses import dataclass, field, KW_ONLY
import enum


class UndefinedSymbol(Exception): ...

class InvalidHeadMovement(Exception): ...


class Motion(enum.Enum):
    L = -1
    S = 0
    R = 1      


@dataclass
class Tape:
    alphabet: set[str]
    content: list[str] = field(default_factory=lambda: ["_"], init=False)
    head: int = field(default=0, init=False)
    size: int = field(default=1, init=False)

    def move_head(self, motion: Motion):
        if not isinstance(motion, Motion):
            raise InvalidHeadMovement
        
        self.head += motion.value
        if not 0 <= self.head < self.size:
            if self.head == -1:
                self.head = 0
            self.content.insert(self.head, "_")
            self.size += 1

    def read(self):
        return self.content[self.head]

    def write(self, symbol: str):
        if symbol not in self.alphabet:
            raise UndefinedSymbol
        self.content[self.head] = symbol

    def load(self, bunch: list):
        if len(bunch) == 0:
            return
        self.head = self.size
        for x in bunch:
            self.content.append(x)
            self.size += 1

    def wipe(self):
        self.content = ["_"]
        self.head = 0
        self.size = 1


@dataclass
class Turing:
    _: KW_ONLY
    states: set[str]
    input_alphabet: set[str]
    tape_alphabet: set[str]
    transition_funcs: dict
    initial_state: str
    accept_state: str

    def __post_init__(self):
        self.current_state = self.initial_state
        self.tape = Tape(self.tape_alphabet)

    def apply_transition(self, qj, write_arg, motion_arg):
        self.current_state = qj
        self.tape.write(write_arg)
        self.tape.move_head(motion_arg)

    def regain_attr(self):
        self.current_state = self.initial_state
        self.tape.wipe()

    def __call__(self, input: list[str]):
        "Runs the specified program on the given input."
        
        self.regain_attr()
        self.tape.load(input)
        while True:
            halted = True

            key = (self.current_state, self.tape.read())
            value = self.transition_funcs.get(key)

            if value:
                halted = False
                self.apply_transition(*value)
            
            if halted:
                if self.current_state == self.accept_state:
                    return True
                else: 
                    return False
    
    
@dataclass
class MultitapeTuring:
    _: KW_ONLY
    states: set[str]
    input_alphabet: set[str]
    tape_alphabet: set[str]
    transition_funcs: list[dict]
    initial_state: str
    accept_state: str

    def __post_init__(self):        
        self.current_state = self.initial_state
        self.tape1 = Tape(self.tape_alphabet)
        self.tape2 = Tape(self.tape_alphabet)

    def apply_transition(self, qj, write_arg1, write_arg2, motion_arg1, motion_arg2):
        self.current_state = qj
        self.tape1.write(write_arg1)
        self.tape1.move_head(motion_arg1)
        self.tape2.write(write_arg2)
        self.tape2.move_head(motion_arg2)

    def regain_attr(self): 
        self.current_state = self.initial_state
        self.tape1.wipe()
        self.tape2.wipe()
        
    def __call__(self, input):
        "Runs the specified program on the given input."
        
        self.regain_attr()
        self.tape1.load(input)
        while True:
            halted = True

            key = (self.current_state, self.tape1.read(), self.tape2.read())
            value = self.transition_funcs.get(key)
            
            if value:
                halted = False
                self.apply_transition(*value)
                
            if halted:
                if self.current_state == self.accept_state:
                    return True
                else:
                    return False
                
                
def convert_transitions(standard: Turing): 
    transitions = {("reject", x, "_"): ("reject", x, standard.initial_state, Motion.S, Motion.S)
                    for x in standard.tape_alphabet}

    for from_, to in standard.transition_funcs.items(): 
        if to[0] == standard.accept_state: 
            transitions[("reject", from_[1], from_[0])] = (
                "accept", to[1], to[0], to[2], Motion.S)
        else: 
            transitions[("reject", from_[1], from_[0])] = (
                "reject", to[1], to[0], to[2], Motion.S)
            
    return transitions
    