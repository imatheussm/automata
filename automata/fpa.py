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

	def process_symbol(self,current_state,symbol,stack_symbol):
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
		return self.process_symbols(current_state,symbol,stack_symbol)

	def process_symbols(self,current_state,symbol,stack_symbol):
		"""Processes from a state to another, considering the symbol to be consumed in the process.

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
		#if isinstance(current_state,tuple) and len(current_state) == 1: current_state = current_state[0]
		try: return self.properties["transitions"][(current_state,symbol,stack_symbol)]
		except: return None

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
		column_titles, space = ["δ"] + list(self.properties["symbols"]) + ["?"], max([len(item) for item in self.properties["transitions"].values()]) * 4 + 2
		column_titles[0] = int((space) / 2) * " " + column_titles[0] + int((space) / 2) * " "
		for (origins, destinations) in self.properties["transitions"].items():
			print(origins)
			if "ε" in origins:
				column_titles.append("ε")
				break
		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in column_titles + ["Γ"]])))
		i, line, previous_state = 1, [], None
		for (state, stack_symbol, symbol) in list(product(self.properties["states"],list(self.properties["stack_symbols"]) + ["?"],column_titles[1:])):
			if line == []:
				if state != previous_state: previous_state, line = state, ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
				else: line = ["{0}{2:^{1}}".format(body_left_margin * " ",space," ")]
			#print("[LINE 116] ({}, {}, {})".format(state,symbol,stack_symbol))
			if i < len(column_titles):
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbols(state,symbol,stack_symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
				if i == len(column_titles)-1: line.append("{1:^{0}}".format(space,stack_symbol))
				i+=1
			else:
				#print("[LINE 128] Final line: {}".format("|".join(["{1:^{0}}".format(space,element) for element in line])))
				string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
				i = 2
				if state != previous_state: previous_state, line = state, ["{0}{2:^{1}}".format(body_left_margin * " ",space,state)]
				else: line = ["{0}{2:^{1}}".format(body_left_margin * " ",space," ")]
				try: line.append("{1:^{0}}".format(space,"{" + ", ".join(list(self.process_symbols(state,symbol,stack_symbol))) + "}"))
				except: line.append("{1:^{0}}".format(space,"ε"))
		string.append(str("|".join(["{1:^{0}}".format(space,element) for element in line])))
		if to_str == True: return "\n".join(string)
		else: print("\n".join(string))