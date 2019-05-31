from automata.finiteAutomaton import finiteAutomaton
class deterministicFiniteAutomaton(finiteAutomaton):
	"""A Deterministic Finite Automaton class to be inherited by the DFA, NFA and NFAE subclasses."""
	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------

		self : deterministicFiniteAutomaton
			A deterministicFiniteAutomaton object.
		properties : dict, str(dict)
			The properties of said automaton. It must be a dictionary object or its string representation.

			Example: {'symbols': ('0', '1'), 'states': ('q0', 'q1'), 'transitions': {('q0', '1'): ('q0',), ('q0', '0'): ('q1',), ('q1', '0'): ('q0',), ('q1', '1'): ('q1',)}, 'initial_state': 'q0', 'final_states': ('q0',)}

			An exception will be raised if the automaton doesn't meet the requirements to be deterministic.
			If you have a .txt file containing the automaton's properties and you want to convert it, use the from_txt() function instead.

		Returns
		-------
		deterministicFiniteAutomaton
			A deterministicFiniteAutomaton object with the stipulated properties.
		"""
		super().__init__(properties)
		for (origins, destinations) in self.properties["transitions"].items():
			if len(destinations) > 1 or "ε" in origins: raise TypeError("This automaton is not deterministic.")