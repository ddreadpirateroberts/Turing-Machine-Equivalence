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


        two_tape_transitions = convert_transitions(self.standard)

        self.multitape = MultitapeTuring(states={"reject", "accept"},
                                         input_alphabet={"a", "b"},
                                         tape_alphabet={"a", "b", "_"}.union(self.standard.states),
                                         transition_funcs=two_tape_transitions,
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
