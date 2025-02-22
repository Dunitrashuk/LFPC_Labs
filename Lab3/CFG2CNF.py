from copy import deepcopy
from re import finditer
from itertools import combinations
from helper import *

productions = {'S': ['aB', 'bA', 'B'], 'A': [
    'b', 'aD', 'AS', 'bAB', ''], 'C': ['AB'], 'B': ['a', 'bS'], 'D': ['BB']}
non = ['S', 'A', 'C', 'B', 'D']
terminal = ['aB', 'bA', 'B', 'b', 'aD', 'AB', 'AS', 'bAB', '', 'a', 'bS', 'BB']


def remove_e(rules):
    rules_copy = deepcopy(rules)
    letters = [1]
    while letters:
        rules = deepcopy(rules_copy)
        letters = []
        for (key, value) in rules.items():
            if '' in value:
                letters.append(key)
        for letter in letters:
            if len(rules[letter]) == 1:
                non.remove(letter)
                for key, value in rules.items():
                    for i, v in enumerate(value):
                        if letter in v:
                            rules_copy[key][i] = v.replace(letter, "")
                del rules_copy[letter]
            else:
                for key, value in rules.items():
                    for v in value:
                        if letter in v:
                            pos = [m.start() for m in finditer(letter, v)]
                            to_remove = []

                            for i in range(1, len(pos)+1):
                                for tupple in list(combinations(pos, i)):
                                    to_remove.append(list(tupple))

                            for indexes in to_remove:
                                v_copy = v[:]

                                for index in indexes:
                                    v_copy = v_copy[:index] + \
                                        " " + v_copy[index+1:]
                                v_copy = v_copy.replace(" ", "")

                                if v_copy not in rules_copy[key]:
                                    rules_copy[key].append(
                                        v_copy.replace(" ", ""))
                rules_copy[letter].remove('')

    return rules_copy


def remove_unit(rules):
    letters = [1]
    while letters:
        letters = []
        for key, value in rules.items():
            for v in value:
                if len(v) == 1 and v in rules.keys():
                    letters.append((key, v))
        for tuppl in letters:
            for rule in rules[tuppl[1]]:
                if rule not in rules[tuppl[0]]:
                    rules[tuppl[0]].append(rule)
            rules[tuppl[0]].remove(tuppl[1])
    return rules


def remove_nonproductive(rules):
    ending = []
    for key, value in rules.items():
        found = False
        for v in value:
            if not any(letter in v for letter in rules.keys()):
                found = True
        if found:
            ending.append(key)

    found = True
    non_ending = []
    while found:
        found = False
        non_ending = list(set(rules.keys()) - set(ending))
        for n in non_ending:
            for v in rules[n]:
                if any(letter in v for letter in ending):
                    found = True
                    ending.append(n)
                    break
    rules_copy = deepcopy(rules)
    for n in non_ending:
        for key, value in rules.items():
            if n == key:
                del rules_copy[key]
                non.remove(key)
                continue
            for v in value:
                if n in v:
                    rules_copy[key].remove(v)
    return rules_copy


def remove_inaccesible(rules):
    start = list(rules.keys())[0]
    accesible = [start]

    for letter in accesible:
        for v in rules[letter]:
            for n in rules.keys():
                if n in v and n not in accesible:
                    accesible.append(n)
    rules_copy = deepcopy(rules)
    for key in rules_copy.keys():
        if key not in accesible:
            del rules[key]
    return rules


def remove_variables(rules):
    X = 'A'
    new_rules = {}
    changes = True
    while changes:
        changes = False
        rules_copy = deepcopy(rules)
        for key, value in rules_copy.items():
            for i, v in enumerate(value):
                variables = splitt(v)
                if len(variables) > 2:
                    changes = True

                    new_X = X + str(len(new_rules)+1)
                    to_replace = "".join(variables[1:])
                    existing = find_key(new_rules, to_replace)
                    if existing:
                        rules[key][i] = variables[0] + existing
                        if key in new_rules.keys():
                            new_rules[key] = variables[0] + existing
                    else:
                        new_rules[new_X] = to_replace
                        rules[key][i] = variables[0] + new_X
                        if key in new_rules.keys():
                            new_rules[key] = variables[0] + new_X
        for key, value in new_rules.items():
            rules[key] = [value]
    return rules


def remove_terminals(rules):
    X = 'B'
    new_rules = {}
    for key, value in rules.items():
        for i, v in enumerate(value):
            variables = splitt(v)
            if len(variables) == 2:
                for letter in variables:
                    if letter not in rules.keys():
                        existing = find_key(new_rules, letter)
                        if existing:
                            rules[key][i] = rules[key][i].replace(
                                letter, existing)
                        else:
                            new_X = X + str(len(new_rules)+1)
                            new_rules[new_X] = letter
                            rules[key][i] = rules[key][i].replace(
                                letter, new_X)
    for key, value in new_rules.items():
        rules[key] = [value]
    return rules


productions = remove_e(productions)
productions = remove_unit(productions)
productions = remove_nonproductive(productions)
productions = remove_inaccesible(productions)
productions = remove_variables(productions)
productions = remove_terminals(productions)

print("\nChomsky Normal Form:")
printt(productions)
