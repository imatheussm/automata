from os import getcwd
from sys import path as sys_path
sys_path.append(getcwd())
from automata import *

#a = finiteAutomaton("./dfa/sample.txt")

a = from_txt("./dfa/dfa2.txt")
b = deterministicFiniteAutomaton(a)

c = from_txt("./nfa/nfa1.txt")
d = nondeterministicFiniteAutomaton(c)

e = from_txt("./nfae/nfae1.txt")
f = nondeterministicFiniteAutomatonWithEMoves(e)

g = from_txt("./nfae/nfae2.txt")
h = nondeterministicFiniteAutomatonWithEMoves(g)

i = from_txt("./fpa/fpa1.txt")
j = deterministicFinitePushdownAutomaton(i)

k = from_txt("./fpa/fpa2.txt")
l = deterministicFinitePushdownAutomaton(k)

m = from_txt("./dfa/dfa1.txt")
n = deterministicFiniteAutomaton(m)

o = from_txt("./fpa/fpa3.txt")
p = finitePushdownAutomaton(o)

q = from_txt("./fpa/fpa4.txt")
r = finitePushdownAutomaton(q)

#from itertools import product
#k_ = list(product(j.properties["states"],j.properties["stack_symbols"],j.properties["symbols"]))