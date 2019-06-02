class finiteAutomaton:
	"""A generic Finite Automaton class to be inherited by the DFA, NFA and NFAE subclasses."""
	def __eq__(self,other):
		"""Checks if two finiteAutomaton objects are the same.

		It will attempt to access the properties dict both provided objects and then compare them. In case it fails to find this attribute or they are not the same, it will return False. Otherwise, True will be returned by it.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		other : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).

		Returns
		-------
		bool
			The result of the comparison.
		"""
		try: return self.properties == other.properties and self.properties["transitions"] == other.properties["transitions"]
		except: return False

	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------

		self : finiteAutomaton
			A finiteAutomaton object.
		properties : dict, str(dict)
			The properties of said automaton. It must be a dictionary object or its string representation.

			Example: {'symbols': ('0', '1'), 'states': ('q0', 'q1'), 'transitions': {('q0', '1'): ('q0',), ('q0', '0'): ('q1',), ('q1', '0'): ('q0',), ('q1', '1'): ('q1',)}, 'initial_state': 'q0', 'final_states': ('q0',)}

			If you have a .txt file containing the automaton's properties and you want to convert it, use the from_txt() function instead.

		Returns
		-------
		finiteAutomaton
			A finiteAutomaton object with the stipulated properties.
		"""
		try: self.properties = dict(properties)
		except: raise TypeError("The properties parameter provided doesnt't seem to be a dictionary.")

	def __repr__(self):
		"""finiteAutomaton general representation.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).

		Returns
		-------
		str
			The string representation of the object, which will be printed out.
		"""
		return "<{} object>\n      Symbols: {}\n       States: {}\n\
  Transitions: {}\nInitial State: {}\n Final States: {}".format(str(type(self)).split("'")[1],
																", ".join(self.properties["symbols"]),
																", ".join(self.properties["states"]),
																str(self.properties["transitions"]),
																self.properties["initial_state"],
																", ".join(self.properties["final_states"]))