# Turing Machine Equivalence Implementation

A Python implementation of the problem from Peter Linz's textbook:

> **Show that every computation that can be done by a standard Turing machine can be done by a multitape machine with a stay-option and at most two states.**

## Implementation

- **Standard TM**: Single tape, multiple states
- **Multitape TM**: Two tapes, only two states (`reject`/`accept`)
- **Key Idea**: Second tape stores the simulated state of the standard TM

## Files

- `turing.py` - Turing machine implementations  
- `turing-test.py` - Equivalence testing and performance comparison

## Usage

```python
from turing_test import Test

test = Test()
test.equivalence()  # Random testing for equivalent behavior
test.runtime()      # Performance comparison
```

## Testing Note

The equivalence check runs 10,000 random inputs to give a loose feeling of equivalence between the machines. This is **not a formal proof** - just empirical validation that both implementations behave similarly on test cases.

## Reference

Based on the theoretical computer science textbook by Peter Linz on formal languages and automata theory.
