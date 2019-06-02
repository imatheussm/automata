from os import getcwd
from sys import path as sys_path
sys_path.append(getcwd())
from automata import *

#a = finiteAutomaton("./dfa/sample.txt")
a = from_txt("./dfa/dfa2.txt")
b = deterministicFiniteAutomaton(a)

c = from_txt("./nfa/nfa1.txt")
d = nondeterministicFiniteAutomaton(c)