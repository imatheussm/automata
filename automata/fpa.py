from automata.fa import *

class finitePushdownAutomaton(finiteAutomaton):
	"""A generic Finite Automaton class to be inherited by the DFPA subclass."""
	def __init__(self,properties):
		"""Class constructor.

		Parameters
		----------
		self : deterministicFinitePushdownAutomaton
			A deterministicFinitePushdownAutomaton object.
		properties : dict, str(dict)
			The properties of said automaton. It must be a dictionary object or its string representation.

			Example: {'symbols': ('0', '1'), 'states': ('q0', 'q1'), 'transitions': {('q0', '1'): ('q0',), ('q0', '0'): ('q1',), ('q1', '0'): ('q0',), ('q1', '1'): ('q1',)}, 'initial_state': 'q0', 'final_states': ('q0',)}

			An exception will be raised if the automaton doesn't meet the requirements to be deterministic.
			If you have a .txt file containing the automaton's properties and you want to convert it into a finiteAutomaton object, use the from_txt() function instead.

		Returns
		-------
		deterministicFinitePushdownAutomaton
			A deterministicFinitePushdownAutomaton object with the stipulated properties.
		"""
		super().__init__(properties)
		if "stack_symbols" not in self.properties.keys(): raise TypeError("The automaton provided does not have a stack.")

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
		string = "({{{}}}, {{{}}}, {}, {}, {{{}}}, {{{}}})".format(", ".join(self.properties["symbols"]),
																   ", ".join(self.properties["states"]),
																   str(transitions),
																   self.properties["initial_state"],
																   ", ".join(self.properties["final_states"]),
																   ", ".join(self.properties["stack_symbols"]))
		if to_str == True: return string
		else: print(string)

	def process_symbol(self,current_state,symbol,stack_symbol,current_stack=None,repr=True):
		"""Redirection to finitePushdownAutomaton.process_symbols() meant to overwrite the superclass' implementation.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		current_state : str
			The current_state.
		symbol : str
			The symbol to be read.
		stack_symbol : str
			The symbol to be read from the stack.

		Returns
		-------
		tuple: (str, str, ..., str) or NoneType
			A tuple containing the new states. If the symbol cannot be processed from the current_state provided, None will be returned.

		"""
		return self.process_symbols(current_state,symbol,stack_symbol,current_stack,repr)

	def process_symbols(self,current_state,symbol,stack_symbol,current_stack=None,repr=True,verbose=False):
		"""Processes from a state to another, considering the symbol to be consumed in the process.
		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		current_state : str
			The current_state.
		symbol : str, tuple(str)
			The symbol (or symbols) to be read.
		stack_symbol : str
			The symbol to be read from the stack.
		Returns
		-------
		tuple: (str, str, ..., str) or NoneType
			A tuple containing the new states. If the symbol cannot be processed from the current_state provided, None will be returned.
		"""
		#if isinstance(current_state,tuple) and len(current_state) == 1:
		#current_state = current_state[0]
		if repr == True:
			try: return self.properties["transitions"][(current_state,symbol,stack_symbol)]
			except: return None
		else:
			new_states = []
			try:
				# [new_state, current_word, current_stack]
				try:
					# (state, symbol, stack)
					if verbose == True: print("δ({}, {}, {}) -> ".format(current_state,symbol[0],current_stack[0]), end="")
					normal_transition = list(self.properties["transitions"][(current_state,symbol[0],current_stack[0])])

					if normal_transition[1] != "ε": normal_transition[1] += current_stack[1:]
					else: normal_transition[1] = current_stack[1:]

					normal_transition = normal_transition[:1] + [symbol[1:]] + normal_transition[1:]
					if verbose == True: print("{}".format(normal_transition))
					new_states.append(tuple(normal_transition))
					del(normal_transition)
				except:
					if verbose == True: print("None")

				try:
					# (state, symbol, ε)
					if verbose == True: print("δ({}, {}, ε) -> ".format(current_state,symbol[0]), end="")
					symbol_empty_transition = list(self.properties["transitions"][(current_state,symbol[0],"ε")])

					if symbol_empty_transition[1] != "ε": symbol_empty_transition[1] += current_stack[:]
					else: symbol_empty_transition[1] = current_stack[:]

					symbol_empty_transition = symbol_empty_transition[:1] + [symbol[1:]] + symbol_empty_transition[1:]
					if verbose == True: print("{}".format(symbol_empty_transition))
					new_states.append(tuple(symbol_empty_transition))
					del(symbol_empty_transition)
				except:
					if verbose == True: print("None")

				try:
					# (state, ε, stack)
					if verbose == True: print("δ({}, ε, {}) -> ".format(current_state,current_stack[0]), end="")
					empty_stack_transition = list(self.properties["transitions"][(current_state,"ε",current_stack[0])])

					if empty_stack_transition[1] != "ε": empty_stack_transition[1] += current_stack[1:]
					else: empty_stack_transition[1] = current_stack[1:]

					empty_stack_transition = empty_stack_transition[:1] + [symbol[:]] + empty_stack_transition[1:]
					if verbose == True: print("{}".format(empty_stack_transition))
					new_states.append(tuple(empty_stack_transition))
					del(empty_stack_transition)
				except:
					if verbose == True: print("None")

				try:
					# (state, ε, ε)
					if verbose == True: print("δ({}, ε, ε) -> ".format(current_state), end="")
					empty_transition = list(self.properties["transitions"][(current_state,"ε","ε")])

					if empty_transition[1] != "ε": empty_transition[1] += current_stack[:]
					else: empty_transition[1] = current_stack[:]

					empty_transition = empty_transition[:1] + [symbol[:]] + empty_transition[1:]
					if verbose == True: print("{}".format(empty_transition))
					new_states.append(tuple(empty_transition))
					del(empty_transition)
				except:
					if verbose == True: print("None")

			except: pass
			if verbose == True: print()
			return tuple(new_states)

	def process_word(self,word,verbose=False,current_states=None):
		"""Checks if a word can be processed by the finiteAutomaton object.

		Parameters
		----------
		self : finiteAutomaton
			An object of the class finiteAutomaton (or any of its subclasses).
		word : str
			The word to be processed.
		verbose : bool (default = False)
			Serves to tell the function if print statements should be displayed as the word is processed.
		current_states : tuple(str), NoneType (default = None)
			The states remaining to be processed. It is actively used throughout the function, since it is recursive.

		Returns
		-------
		bool
			The result of the processing. In other words: if the word has been accepted by the automaton or not.
		"""
		is_final = False

		if current_states == None: current_states = ((self.properties["initial_state"],word,""),)

		if verbose == True: print("current_states -> {}".format(current_states))

		new_states = []

		for current_state in current_states:
			if verbose == True: print("current_state -> {}".format(current_state))
			if len(current_state[1]) > 0:
				new_states += list(self.process_symbols(current_state[0],current_state[1],"",current_state[2],False,verbose))
			else: new_states.append(current_state)

		for new_state in new_states:
			if len(new_state[1]) > 0: return self.process_word(word,verbose,new_states)

		if verbose==True:
			print("The word has been entirely processed in all alternatives.")
			print("Final result: {}".format(new_states))
			print("Verifying if the final transition is possible to each state...")

		for final_state in new_states:
			if verbose == True: print("δ({}, {}, {}) -> ".format(final_state[0],final_state[1] if len(final_state[1])>0 else "ε",final_state[2] if len(final_state[2]) > 0 else "ε"), end="")
			if len(final_state[1])==0 and len(final_state[2])==0:
				try:
					if verbose==True: print(self.properties["transitions"][(final_state[0],"?","?")])
					is_final = True
				except:
					if verbose==True: print("None")
			else:
				if verbose ==True: print("None")

		if verbose == True: print("The function returns ", end="")
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
		column_titles, stack_symbols, space = ["δ"] + list(self.properties["symbols"]) + ["?"], list(self.properties["stack_symbols"]) + ["?"], max([len(item) for item in self.properties["transitions"].values()]) * 4 + 2
		column_titles[0] = int((space) / 2) * " " + column_titles[0] + int((space) / 2) * " "
		for origins in self.properties["transitions"].keys():
			if origins[1] == "ε":
				column_titles.append("ε")
				break
		for origins in self.properties["transitions"].keys():
			if origins[2] == "ε":
				stack_symbols.append("ε")
				break

		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in column_titles + ["Γ"]])))
		i, line, previous_state = 1, [], None
		for (state, stack_symbol, symbol) in list(product(self.properties["states"],stack_symbols,column_titles[1:])):
			if line == []:
				if state != previous_state: previous_state, line = state, ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
				else: line = ["{0}{2:^{1}}".format(body_left_margin * " ",space," ")]
			#print("[LINE 116] ({}, {}, {})".format(state,symbol,stack_symbol))
			if i < len(column_titles):
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbols(state,symbol,stack_symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
				if i == len(column_titles) - 1: line.append("{1:^{0}}".format(space,stack_symbol))
				i+=1
			else:
				#print("[LINE 128] Final line:
				#{}".format("|".join(["{1:^{0}}".format(space,element) for element in
				#line])))
				string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
				i = 2
				if state != previous_state: previous_state, line = state, ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
				else: line = ["{0}{2:^{1}}".format(body_left_margin * " ",space," ")]
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbols(state,symbol,stack_symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
		if to_str == True: return "\n".join(string)
		else: print("\n".join(string))