class finiteAutomaton:
	"""A generic Finite Automaton class to be inherited by the DFA, NFA and NFAE subclasses."""
	def __init__(self,automaton):
		"""Class constructor.

		Parameters
		----------

		Returns
		-------
		"""
		self.properties = {"symbols":"",
						   "states":"",
						   "transitions":"",
						   "initial_state":"",
						   "final_states":""}
		self.tuple_order = ["symbols",
							"states",
							"transitions",
							"initial_state",
							"final_states"]
		with open(automaton,"r") as file:
			print("File opened.")
			# loading the properties of the automaton
			properties_string = file.readline().strip("\n")[1:-1]
			print("Properties line: {}".format(properties_string))
			if properties_string[0] != "{" or properties_string[-1] != "}": raise SyntaxError("The automaton properties tuple ({}) is incorrectly formatted.".format(properties_string))

			current_property, index = 0, 0
			print("[Line 30] First property: {}".format(self.tuple_order[current_property]))
			while index < len(properties_string):
				if properties_string[index] == "{":
					while properties_string[index] != "}":
						self.properties[self.tuple_order[current_property]] += properties_string[index]
						index += 1
					self.properties[self.tuple_order[current_property]] += properties_string[index]
					index += 1
					current_property += 1
					print("[Line 40] self.properties[{}]: {}".format(self.tuple_order[current_property - 1],self.properties[self.tuple_order[current_property - 1]]))
					try: print("[Line 41] Next property: {}".format(self.tuple_order[current_property]))
					except:
						print("[Line 43] Properties fully loaded as strings.")
						break
				elif properties_string[index] == "," or properties_string[index] == " ": index+=1
				else:
					while properties_string[index] != ",":
						self.properties[self.tuple_order[current_property]] += properties_string[index]
						index += 1
					current_property+=1
					print("[Line 51] self.properties[{}]: {}".format(self.tuple_order[current_property - 1],self.properties[self.tuple_order[current_property - 1]]))
					print("[Line 52] Next property: {}".format(self.tuple_order[current_property]))
			print(self.properties)