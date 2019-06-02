from automata.fa import finiteAutomaton

class nondeterministicFiniteAutomatonWithEMoves(finiteAutomaton):
	"""A Nondeterministic Finite Automaton with ε-Moves class which inherits from finiteAutomaton."""
	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------
		self : nondeterministicFiniteAutomatonWithEMoves
			A nondeterministicFiniteAutomatonWithEMoves object.
		properties : dict, str(dict)
			The properties of said automaton. It must be a dictionary object or its string representation.

			Example: {'symbols': ('0', '1'), 'states': ('q0', 'q1'), 'transitions': {('q0', '1'): ('q0',), ('q0', '0'): ('q1',), ('q1', '0'): ('q0',), ('q1', '1'): ('q1',)}, 'initial_state': 'q0', 'final_states': ('q0',)}

			An exception will be raised if the automaton doesn't meet the requirements to be deterministic.
			If you have a .txt file containing the automaton's properties and you want to convert it into a finiteAutomaton object, use the from_txt() function instead.

		Returns
		-------
		nondeterministicFiniteAutomatonWithEMoves
			A nondeterministicFiniteAutomatonWithEMoves object with the stipulated properties.
		"""
		super().__init__(properties)
		empty_moves = False
		for (origins, destinations) in self.properties["transitions"].items():
			if "ε" in origins: empty_moves = True
		if empty_moves == False: raise TypeError("This automaton does not have ε-moves.")
		else: del(empty_moves)