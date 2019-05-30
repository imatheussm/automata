<p align="center"><img src="../igor-matheus.png"></img></p>

# Nondeterministic Finite Automatons (NFA)

**No empty moves yet; however, now you can have multiple transitions from a single state.**

According to [Wikipedia](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton), a NFA, unlike a DFA, does not need to abide by the rules that characterize it. Just for reference, a DFA must obbey the following rules:

- each of its transitions is uniquely determined by its source state and input symbol; and
- reading an input symbol is required for each state transition.

We can infer, therefore, that a [NFA with ε-moves](../nfae) is just a "flavor" of the NFA.