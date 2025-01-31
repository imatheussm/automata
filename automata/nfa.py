﻿from automata.fa import finiteAutomaton

class nondeterministicFiniteAutomaton(finiteAutomaton):
	"""A Nondeterministic Finite Automaton class which inherits from finiteAutomaton."""
	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------
		self : nondeterministicFiniteAutomaton
			A nondeterministicFiniteAutomaton object.
		properties : dict, str(dict)
			The properties of said automaton. It must be a dictionary object or its string representation.

			Example: {'symbols': ('0', '1'), 'states': ('q0', 'q1'), 'transitions': {('q0', '1'): ('q0',), ('q0', '0'): ('q1',), ('q1', '0'): ('q0',), ('q1', '1'): ('q1',)}, 'initial_state': 'q0', 'final_states': ('q0',)}

			An exception will be raised if the automaton doesn't meet the requirements to be deterministic.
			If you have a .txt file containing the automaton's properties and you want to convert it into a finiteAutomaton object, use the from_txt() function instead.

		Returns
		-------
		nondeterministicFiniteAutomaton
			A nondeterministicFiniteAutomaton object with the stipulated properties.
		"""
		super().__init__(properties)
		is_nondeterministic = False
		for (origins, destinations) in self.properties["transitions"].items():
			if len(destinations) > 1: is_nondeterministic = True
			if "ε" in origins: raise TypeError("The automaton provided has ε-moves.")
		if not is_nondeterministic: raise TypeError("The automaton provided is deterministic.")
		else: del(is_nondeterministic)