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

	def process_symbol(self,current_state,symbol):
		"""Processes from a state to another, considering the symbol to be consumed in the process.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		current_state : str
			The current_state.
		symbol : str
			The symbol to be read.

		Returns
		-------
		tuple: (str, str, ..., str) or NoneType
			A tuple containing the new states. If the symbol cannot be processed from the current_state provided, None will be returned.
		"""
		try: return self.properties["transitions"][(current_state,symbol)]
		except: return None

	def process_word(self,word,current_states=None,verbose=False):
		"""Checks if a word can be processed by the finiteAutomaton object.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		word : str
			The word to be processed.
		current_states : tuple(str), str, NoneType (default = None)
			The state to be processed.
		verbose : bool
			Serves to tell the function if print statements should be displayed as the word is processed.

		Returns
		-------
		bool
			The result of the processing. In other words: if the word has been accepted by the automaton or not.
		"""
		is_final = False

		if current_states == None: current_states = (self.properties["initial_state"],)
		if verbose==True: print("[LINE 102] Current state (s): {}".format(current_states))
		if word[0] not in self.properties["symbols"]: raise ValueError("The word provided contains symbols which are not in this automaton's alphabet.")
		new_current_states = []
		for current_state in current_states:
			if verbose==True: print("[LINE 106] Attempting to process ({},{})".format(current_state,word[0]))
			try: new_current_states += list(self.process_symbol(current_state,word[0]))
			except: pass
		current_states = tuple(new_current_states)
		del(new_current_states)
		if len(word) > 1:
			if verbose==True: print("[LINE 111] Remaining symbols to be processed: {}\n".format(word[1:]))
			return self.process_word(word[1:],current_states=current_states,verbose=verbose)
		else:
			if verbose==True: print("\n\n[LINE 114] Final states found: {}\n".format(current_states))
			for state in current_states:
				if state in self.properties["final_states"]:
					if verbose==True: print("[LINE 117] The state {} is final.".format(state))
					is_final = True
				else:
					if verbose==True: print("[LINE 119] The state {} is not final.".format(state))
			if is_final == True:
				if verbose==True: print("\n[LINE 120] The word has been accepted. The function returns ",end="")
			else:
				if verbose==True: print("\n[LINE 121] The word has not been accepted. The function returns ",end="")
			return is_final