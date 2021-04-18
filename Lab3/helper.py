def find_key(rule, value):
    for key, v in rule.items():
        if v == value:
            return key
    return None


def splitt(string):
    splitted = []
    old_s = ''
    for s in string:
        if s.isdigit():
            old_s += s
        else:
            splitted.append(old_s)
            old_s = s
    splitted.remove('')
    splitted.append(old_s)
    return splitted


def printt(rules):
    for key, value in rules.items():
        print(key + " -> " + value[0], end=' ')
        for v in value[1:]:
            print("| " + v, end=' ')
        print()
