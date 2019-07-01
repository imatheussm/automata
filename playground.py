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

i2 = from_txt("./fpa/fpa1_dashed.txt")
j2 = deterministicFinitePushdownAutomaton(i2)

k = from_txt("./fpa/fpa2.txt")
l = deterministicFinitePushdownAutomaton(k)

k2 = from_txt("./fpa/fpa2_dashed.txt")
l2 = deterministicFinitePushdownAutomaton(k2)

m = from_txt("./dfa/dfa1.txt")
n = deterministicFiniteAutomaton(m)

o = from_txt("./fpa/fpa3.txt")
p = finitePushdownAutomaton(o)

o2 = from_txt("./fpa/fpa3_dashed.txt")
p2 = finitePushdownAutomaton(o2)

q = from_txt("./fpa/fpa4.txt")
r = finitePushdownAutomaton(q)


# a^mb^na^(m+n)
q2 = from_txt("./fpa/fpa4_dashed.txt")
r2 = finitePushdownAutomaton(q2)

eduardo1 = from_txt("D:\igor\OneDrive\Documentos\GitHub\hephaestus\samples\mirror.automat")
eduardo2 = finitePushdownAutomaton(eduardo1)

#from itertools import product
#k_ = list(product(j.properties["states"],j.properties["stack_symbols"],j.properties["symbols"]))