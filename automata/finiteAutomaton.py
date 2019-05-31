class finiteAutomaton:
	"""A generic Finite Automaton class to be inherited by the DFA, NFA and NFAE subclasses."""
	def __init__(self,automaton,verbose=False):
		"""Class constructor.

		Parameters
		----------

		Returns
		-------
		"""
		self.tuple_order = ["symbols", "states", "transitions", "initial_state", "final_states"]
		self.properties  = {item: "" for item in self.tuple_order}

		with open(automaton,"r") as file:
			# Opening the file and obtaining the automaton file's properties line
			if verbose==True: print("File opened.")
			properties_string = file.readline().strip("\n")[1:-1]
			if verbose==True: print("Properties line: {}".format(properties_string))
			if properties_string[0] != "{" or properties_string[-1] != "}": raise SyntaxError("The automaton properties tuple ({}) is incorrectly formatted.".format(properties_string))

			# Separating the string.
			current_property, index = 0, 0
			if verbose==True: print("[Line 29] First property: {}".format(self.tuple_order[current_property]))
			while index < len(properties_string):
				if properties_string[index] == "{":
					while properties_string[index] != "}":
						self.properties[self.tuple_order[current_property]] += properties_string[index]
						index += 1
					self.properties[self.tuple_order[current_property]] += properties_string[index]
					index += 1
					current_property += 1
					if verbose==True: print("[Line 38] self.properties[{}]: {}".format(self.tuple_order[current_property - 1],self.properties[self.tuple_order[current_property - 1]]))
					try:
						if verbose==True: print("[Line 40] Next property: {}".format(self.tuple_order[current_property]))
						elif current_property>=len(self.tuple_order): raise IndexError()
					except:
						if verbose==True: print("[Line 43] Properties fully loaded as strings.")
						break
				elif properties_string[index] == "," or properties_string[index] == " ": index+=1
				else:
					while properties_string[index] != ",":
						self.properties[self.tuple_order[current_property]] += properties_string[index]
						index += 1
					current_property+=1
					if verbose==True: print("[Line 51] self.properties[{}]: {}".format(self.tuple_order[current_property - 1],self.properties[self.tuple_order[current_property - 1]]))
					if verbose==True: print("[Line 52] Next property: {}".format(self.tuple_order[current_property]))
			if verbose==True: print(self.properties)

			# Separating the lists contained inside the tuple
			for item in self.tuple_order:
				if self.properties[item][0] == "{" and self.properties[item][-1] == "}": self.properties[item] = tuple(self.properties[item][1:-1].split(", "))

			if verbose==True: print(self.properties)

			# Processing the transitions
			transitions = {}
			transition_strings = [line.strip("\n").split(", ") for line in file.readlines()]
			for item in transition_strings:
				if (item[0],item[1]) not in transitions.keys(): transitions[(item[0],item[1])] = []
				transitions[(item[0],item[1])].append(item[2])
			if verbose==True: print(transitions)
			for transition in transitions.keys(): transitions[transition] = tuple(transitions[transition])

			self.properties["transitions"] = transitions

			# Deleting unnecessary variables from memory
			del(properties_string,current_property,index,transition_strings,transitions)

			if verbose==True: print(self.properties)

	def __repr__(self):
		return "<finiteAutomaton object>\n      Symbols: {}\n       States: {}\n\
  Transitions: {}\nInitial State: {}\n Final States: {}".format(", ".join(self.properties["symbols"]),
																", ".join(self.properties["states"]),
																str(self.properties["transitions"]),
																self.properties["initial_state"],
																", ".join(self.properties["final_states"]))