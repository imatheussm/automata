from automata.dfa import *
from automata.nfa import *
from automata.nfae import *

def from_txt(automaton,verbose=False):
	"""Converts a .txt file containing the automaton's properties into a finiteAutomaton (sub)class.

	Parameters
	----------
	automaton : str (path)
		The path to the .txt file containing the automaton's properties.

		Example: ({0, 1}, {q0, q1}, S, q0, {q0})
				 q0, 1, q0
				 q0, 0, q1
				 q1, 0, q0
				 q1, 1, q1
	verbose : bool (default = False)
		If set to True, useful information about the treatment process will be printed as the function deals with the automaton file.

	Returns
	-------
	finiteAutomaton, deterministicFiniteAutomaton, nondeterministicFiniteAutomaton, nondeterministicFiniteAutomatonWithEMoves
		An automaton object of one of the aforementioned (sub)classes, depending on the properties stipulated.
	"""

	order = ["symbols", "states", "transitions", "initial_state", "final_states"]
	properties = {item: "" for item in order}

	with open(automaton,"r") as file:
		# Opening the file and obtaining the automaton file's properties line
		if verbose == True: print("File opened.")
		properties_string = file.readline().strip("\n")[1:-1]
		if verbose == True: print("Properties line: {}".format(properties_string))
		if properties_string[0] != "{" or properties_string[-1] != "}": raise SyntaxError("The automaton properties tuple ({}) is incorrectly formatted.".format(properties_string))

		# Separating the string.
		current_property, index = 0, 0
		if verbose == True: print("[Line 29] First property: {}".format(order[current_property]))
		while index < len(properties_string):
			if properties_string[index] == "{":
				while properties_string[index] != "}":
					properties[order[current_property]] += properties_string[index]
					index += 1
				properties[order[current_property]] += properties_string[index]
				index += 1
				current_property += 1
				if verbose == True: print("[Line 38] properties[{}]: {}".format(order[current_property - 1],properties[order[current_property - 1]]))
				try:
					if verbose == True: print("[Line 40] Next property: {}".format(order[current_property]))
					elif current_property >= len(order): raise IndexError()
				except:
					if verbose == True: print("[Line 43] Properties fully loaded as strings.")
					break
			elif properties_string[index] == "," or properties_string[index] == " ": index+=1
			else:
				while properties_string[index] != ",":
					properties[order[current_property]] += properties_string[index]
					index += 1
				current_property+=1
				if verbose == True: print("[Line 51] properties[{}]: {}".format(order[current_property - 1],properties[order[current_property - 1]]))
				if verbose == True: print("[Line 52] Next property: {}".format(order[current_property]))
		if verbose == True: print(properties)

		# Separating the lists contained inside the tuple
		for item in order:
			if properties[item][0] == "{" and properties[item][-1] == "}": properties[item] = tuple(properties[item][1:-1].split(", "))

		if verbose == True: print(properties)

		# Processing the transitions
		transitions = {}
		transition_strings = [item.strip("\n").split(", ") for item in file.readlines()]
		for item in transition_strings:
			if (item[0],item[1]) not in transitions.keys(): transitions[(item[0],item[1])] = []
			transitions[(item[0],item[1])] += item[2:]
		if verbose == True: print(transitions)
		for transition in transitions.keys(): transitions[transition] = tuple(transitions[transition])

		properties["transitions"] = transitions

		# Deleting unnecessary variables from memory
		del(properties_string,current_property,index,transition_strings,transitions,order)

		if verbose == True: print(properties)

		return properties