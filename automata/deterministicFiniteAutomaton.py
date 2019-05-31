from automata.finiteAutomaton import finiteAutomaton
class deterministicFiniteAutomaton(finiteAutomaton):
	"""A Deterministic Finite Automaton class to be inherited by the DFA, NFA and NFAE subclasses."""
	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------

		Returns
		-------
		"""
		super().__init__(properties)
		for (origins, destinations) in self.properties["transitions"].items():
			if len(destinations)>1 or "ε" in origins: raise TypeError("This automaton is not deterministic.")