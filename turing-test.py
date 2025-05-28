from turing import Turing, MultitapeTuring, Motion, convert_transitions
import time
import random


class Test:
    def __init__(self):
        self.input = ["a" for _ in range(100000)] + ["b"]

        single_tape_transitions = {("q0", "a"): ("q1", "a", Motion.R),
                                   ("q0", "b"): ("qf", "b", Motion.L),
                                   ("q0", "_"): ("qf", "_", Motion.L),
                                   ("q1", "a"): ("q1", "a", Motion.R),
                                   ("q1", "_"): ("qf", "_", Motion.L)}

        self.standard = Turing(states={"q0", "q1", "qf"},
                               input_alphabet={"a", "b"},
                               tape_alphabet={"a", "b", "_"},
                               transition_funcs=single_tape_transitions,
                               initial_state="q0",
                               accept_state="qf")

        initialize = {("reject", x, "_"): ("reject", x, self.standard.initial_state, Motion.S, Motion.S)
                      for x in self.standard.tape_alphabet}

        two_tape_transitions = {("reject", "a", "q0"): ("reject", "a", "q1", Motion.R, Motion.S),
                                ("reject", "b", "q0"): ("accept", "b", "qf", Motion.L, Motion.S),
                                ("reject", "_", "q0"): ("accept", "_", "qf", Motion.L, Motion.S),
                                ("reject", "a", "q1"): ("reject", "a", "q1", Motion.R, Motion.S),
                                ("reject", "_", "q1"): ("accept", "_", "qf", Motion.L, Motion.S)}

        self.multitape = MultitapeTuring(states={"reject", "accept"},
                                         input_alphabet={"a", "b"},
                                         tape_alphabet={"a", "b", "_"}.union(self.standard.states),
                                         transition_funcs=initialize|two_tape_transitions,
                                         initial_state="reject",
                                         accept_state="accept")

    def makeup_test_subject(self):
        subject = []
        for _ in range(1000):
            subject.append(random.choice(["a", "b"]))
        return subject

    def equivalence(self):
        for _ in range(10000):
            random_entry = self.makeup_test_subject()
            assert self.standard(random_entry) == self.multitape(random_entry), "There is a problem"
        print("All Good")

    def runtime(self, cycle=20):      
        res = {"Standard": 0, "Multitape": 0}
        
        print(self.standard(self.input), self.multitape(self.input))
        for _ in range(cycle):
            start = time.time()
            self.standard(self.input)
            res["Standard"] += time.time() - start

            start = time.time()
            self.multitape(self.input)
            res["Multitape"] += time.time() - start

        res = {i: j/cycle for i, j in res.items()}
        print(res)


test = Test()
test.equivalence()
test.runtime()
