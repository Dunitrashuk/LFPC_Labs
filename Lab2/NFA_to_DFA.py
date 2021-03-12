# siant 18

# S -> aA | aS
# A -> bB
# B -> aB | bC
# C -> aC | empty

import pandas as pd

nfa = {'S': {'a': ['S', 'A'], 'b': [], 'c': []}, 'A': {'a': [], 'b': ['B'], 'c': [
]}, 'B': {'a': ['B'], 'b': ['C'], 'c': []}, 'C': {'a': ['C'], 'b': [], 'c': []}}

n = 4
t = 3

nfa_table = pd.DataFrame(nfa).transpose()
print("\nNFA table: ")
print(nfa_table)

nfa_final_state = ['C']
new_states_list = []
dfa = {}

keys_list = list(list(nfa.keys())[0])
edge_list = list(nfa[keys_list[0]].keys())
dfa[keys_list[0]] = {}

for i in range(t):
    s = "".join(nfa[keys_list[0]][edge_list[i]])
    dfa[keys_list[0]][edge_list[i]] = s
    if s not in keys_list:
        new_states_list.append(s)
        keys_list.append(s)

while len(new_states_list) != 0:
    dfa[new_states_list[0]] = {}
    for _ in range(len(new_states_list[0])):
        for i in range(len(edge_list)):
            temp = []
            for j in range(len(new_states_list[0])):
                temp += nfa[new_states_list[0][j]][edge_list[i]]
            s = ""
            s = s.join(temp)
            if s not in keys_list:
                new_states_list.append(s)
                keys_list.append(s)
            dfa[new_states_list[0]][edge_list[i]] = s

    new_states_list.remove(new_states_list[0])

print("\nDFA \n")
print(dfa)
print("\nDFA table: ")
dfa_table = pd.DataFrame(dfa).transpose()
print(dfa_table)
