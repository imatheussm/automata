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

	def process_symbols(self,current_state,symbol,stack_symbol,current_stack=None,repr=True):
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
		if repr==True:
			try: return self.properties["transitions"][(current_state,symbol,stack_symbol)]
			except: return None
		else:
			try:
				result = self.properties["transitions"][(current_state,symbol,stack_symbol)]
				if symbol=="?" and stack_symbol=="?" and current_stack=="": return (result[0],current_stack)
				if stack_symbol=="ε":
					if result[1]=="ε": return (result[0], current_stack)
					else: return (result[0], result[1] + current_stack[1:])
				else:
					if result[1]=="ε": return (result[0], current_stack[1:])
					else: return (result[0], result[1] + current_stack[1:])
			except: return None

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
		current_states : tuple(str), str, NoneType (default = None)
			The states remaining to be processed. It is actively used throughout the function, since it is recursive.
		current_stack : str, NoneType (default = None)
			The content of the stack. It is actively used throughout the function, since it is recursive.

		Returns
		-------
		bool
			The result of the processing. In other words: if the word has been accepted by the automaton or not.

		To-do
		-----
		- Contemplate the empty stack-reads along with the empty word-reads
			This will be tricky, since there is four possibilities (len((symbol, empty))*len((empty, symbol))). To do this, I have to verify the existance of ε-moves word- and stack-related. More complexity!
		- Implement more verbose prints (stack status as well!)
			I would do this anyway, since it will be far less painful to debug as I develop this function. Among these stack prints, I will have to print the stack as well, which is another element worth verifying. For the sake of convenience, it must have a pointer to the top of the stack, to avoid misinterpreting conventions by both my and my professor's part.
		- Proceed with the goddamn proof-testing
			This will be the most delightful (or dreadful and painful) phase: see the returned movements and check manually if they are correct. And I have to do this to every single one of the remaining automaton types.
		"""
		is_final = False

		if current_states == None: current_states = ((self.properties["initial_state"],""),)

		new_states = []
		if len(word)>0:
			for (current_state, current_stack) in current_states:
				if verbose==True: print("\n[LINE 142] current_state: {} | current_stack: {} | word: {}".format(current_state,current_stack,word))
				# CASO (current_state,"ε","ε")
				if verbose==True: print("[LINE 145] Attempting to add ({}, \"ε\", \"ε\"). Result: {}".format(current_state,self.process_symbols(current_state,"ε","ε",current_stack,False)))
				try:
					intermediate_state = self.process_symbols(current_state,"ε","ε",current_stack,False)
					if verbose==True: print("[LINE 152] Now, processing ({}, {}, \"ε\")".format(intermediate_state[0], word[0], "ε", intermediate_state[1],False))
					try: new_states.append(self.process_symbols(intermediate_state[0],word[0],"ε",intermediate_state[1],False))
					except: pass
					if verbose==True: print("[LINE 152] Now, processing ({}, {}, {})".format(intermediate_state[0], word[0], intermediate_state[1][0], intermediate_state[1],False))
					try: new_states.append(self.process_symbols(intermediate_state[0],word[0],intermediate_state[1][0],intermediate_state[1],False))
					except: pass

				except: pass
				# CASO (current_state,word[0],"ε")
				if verbose==True: print("[LINE 149] Attempting to add ({}, {}, \"ε\"). Result: {}".format(current_state,word[0],self.process_symbols(current_state,word[0],"ε",current_stack,False)))
				try: new_states.append(self.process_symbols(current_state,word[0],"ε",current_stack,False))
				except: pass
				# CASO (current_state,"ε",current_stack[0])
				if len(current_stack)>0:
					if verbose==True: print("[LINE 153] There's something in the stack! Stack: {}".format(current_stack))
					if verbose==True: print("[LINE 145] Attempting to add ({}, \"ε\", {}). Result: {}".format(current_state,current_stack[0],self.process_symbols(current_state,"ε","ε",current_stack,False)))
					try: new_states.append(self.process_symbols(current_state,"ε",current_stack[0],current_stack,False))
					except: pass
					# CASO (current_state,word[0],current_stack[0])
					if verbose==True: print("[LINE 156] Attempting to add ({}, {}, {}). Result: {}".format(current_state,word[0],current_stack[0],self.process_symbols(current_state,word[0],current_stack[0],current_stack,False)))
					try: new_states.append(self.process_symbols(current_state,word[0],current_stack[0],current_stack,False))
					except: pass
			new_states = tuple(set([item for item in new_states if item != None]))
			if verbose==True: print("[LINE 159] Result of this round: {}.".format(new_states))
			return self.process_word(word[1:],verbose,new_states)
		else:
			# CASO (len(word==0))
			for (current_state, current_stack) in current_states:
				if verbose==True: print("The word has been entirely processed. Verifying if the final transition is possible through ({}, \"?\", \"?\")".format(current_state))
				if (current_state, "?", "?") in self.properties["transitions"].keys():
					if len(current_stack)==0:
						if verbose==True: print("[LINE 145] Attempting to add ({}, \"?\", \"?\"). Result: {}".format(current_state,self.process_symbols(current_state,"?","?",current_stack,False)))
						new_states.append(self.process_symbols(current_state,"?","?",current_stack,False))

		for (final_state,final_stack) in new_states:
			if verbose==True: print("Evaluating state {}, with stack = {}... ".format(final_state,final_stack),end="")
			if final_stack=="" and final_state in self.properties["final_states"]:
				if verbose==True: print("This state is considered final.")
				is_final=True
			else:
				if verbose==True: print("This state is not considered final.")

		if verbose==True: print("The function returns ", end="")
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
			if origins[1]=="ε":
				column_titles.append("ε")
				break
		for origins in self.properties["transitions"].keys():
			if origins[2]=="ε":
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