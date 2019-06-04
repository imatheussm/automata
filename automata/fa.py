from itertools import product

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

	def __repr__(self,alt_display=True):
		"""finiteAutomaton general representation.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		alt_display : bool
			Serves to tell the method if you want the extended version of the representation by default or not.

		Returns
		-------
		str
			The string representation of the object, which will be printed out.
		"""
		if alt_display == True: return "<{} object>\n  Automaton: {}\nTransitions: {}".format(str(type(self)).split("'")[1],
																							   self.automaton(False,True),
																							   self.transitions(True,14))
		return "<{} object>\n      Symbols: {}\n       States: {}\n\
  Transitions: {}\nInitial State: {}\n Final States: {}".format(str(type(self)).split("'")[1],
																", ".join(self.properties["symbols"]),
																", ".join(self.properties["states"]),
																str(self.properties["transitions"]),
																self.properties["initial_state"],
																", ".join(self.properties["final_states"]))

	def __str__(self):
		"""String representation of the automaton.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).

		Returns
		-------
		str
			The string representation of the automaton.
		"""
		return self.automaton(True,True)

	def automaton(self,transitions=False,to_str=False):
		"""Prints the automaton's properties.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		transitions : bool (default = False)
			This serves to tell the method to print the transitions instead of just their placeholder (δ).
		to_str : bool (default = False)
			This serves to tell the method to print a string object to be returned instead of just printing the transitions.
		Returns
		-------
		str, void
			Returns a string if to_str == True; otherwise, it just prints it and doesn't return anything.
		"""
		if transitions == True: transitions = self.properties["transitions"]
		else: transitions = "δ"
		string = "({{{}}}, {{{}}}, {}, {}, {{{}}})".format(", ".join(self.properties["symbols"]),
																					 ", ".join(self.properties["states"]),
																					 str(transitions),
																					 self.properties["initial_state"],
																					 ", ".join(self.properties["final_states"]))
		if to_str == True: return string
		else: print(string)

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
		if isinstance(current_state,tuple) and len(current_state) == 1: current_state = current_state[0]
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
			The state to be processed. It is actively used throughout the function, since it is recursive.
		verbose : bool
			Serves to tell the function if print statements should be displayed as the word is processed.

		Returns
		-------
		bool
			The result of the processing. In other words: if the word has been accepted by the automaton or not.
		"""
		is_final = False

		if current_states == None: current_states = (self.properties["initial_state"],)
		if verbose == True: print("[LINE 102] Current state (s): {}".format(", ".join(current_states)))
		if word[0] not in self.properties["symbols"]:
			if verbose == True: print("\n[LINE 163] The symbol {} is not contained in this automaton's alphabet. As such, it cannot be processed.\n\
[LINE 164] The function returns ".format(word[0]),
										 end="")
			return False
		new_current_states = []
		for current_state in current_states:
			if (current_state, "ε") in self.properties["transitions"].keys():
				if verbose == True:
					print("[LINE 171] This state has the empty transition. All possibilities shall be tested.")
					print("[LINE 172] Executing δ({{{}}}, ε) and δ({}, {})".format(current_state,"{" + "".join(str(self.process_symbol(current_state,"ε"))[1:-1].strip(",").split("'")) + "}",word[0]))
				try: new_current_states += list(self.process_symbol(self.process_symbol(current_state,"ε"),word[0]))
				except: pass
				if verbose == True:
					print("[LINE 175] Executing δ({{{}}}, {}) and δ({}, ε)".format(current_state,word[0],"{" + "".join(str(self.process_symbol(current_state,word[0]))[1:-1].strip(",").split("'")) + "}"))
				try: new_current_states += list(self.process_symbol(self.process_symbol(current_state,word[0]),"ε"))
				except: pass
			if verbose == True: print("[LINE 178] Executing δ({{{}}}, {})\n".format(current_state,word[0]))
			try: new_current_states += list(self.process_symbol(current_state,word[0]))
			except: pass
		current_states = tuple(sorted(set(new_current_states)))
		del(new_current_states)
		if len(word) > 1:
			if verbose == True: print("[LINE 184] Remaining symbols to be processed: {}\n".format(word[1:]))
			return self.process_word(word[1:],current_states=current_states,verbose=verbose)
		else:
			if verbose == True: print("\n[LINE 187] Final states found: {}\n".format(", ".join(current_states)))
			for state in current_states:
				if state in self.properties["final_states"]:
					if verbose == True: print("[LINE 190] {} is final.".format(state))
					is_final = True
				else:
					if verbose == True: print("[LINE 193] {} is not final.".format(state))
			if is_final == True:
				if verbose == True: print("\n[LINE 195] The word has been accepted. The function returns ",end="")
			else:
				if verbose == True: print("\n[LINE 197] The word has not been accepted. The function returns ",end="")
			return is_final

	def transitions(self,to_str=False,body_left_margin=0):
		"""Prints the transitions in a transition table format.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		to_str : bool (default = False)
			This serves to tell the method if you want a string object to be returned instead of just printing the transitions.
		body_left_margin : int (default = 0)
			This parameter, if changed, will define the spacing of the second line onwards (body). It is used with .__repr__() to better display the automaton.
		Returns
		-------
		str, void
			Returns a string if to_str == True; otherwise, it just prints it and doesn't return anything.
		"""
		string = []
		column_titles, space = ["δ"] + list(self.properties["symbols"]), max([len(item) for item in self.properties["transitions"].values()]) * 4 + 2
		column_titles[0] = int((space) / 2) * " " + column_titles[0] + int((space) / 2) * " "
		for (origins, destinations) in self.properties["transitions"].items():
			if "ε" in origins:
				column_titles.append("ε")
				break
		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in column_titles])))
		i, line = 1, []
		for (state, symbol) in list(product(self.properties["states"],column_titles[1:])):
			if line == []: line = ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
			if i < len(column_titles):
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbol(state,symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
				i+=1
			else:
				string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
				i,line = 2, ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbol(state,symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
		if to_str == True: return "\n".join(string)
		else: print("\n".join(string))