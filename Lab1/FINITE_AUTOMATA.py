# Variant 18.
# VN={S, A, B, C}
# VT={a, b}
# P={1. S->aA
#    2. A->bS
#    3. S->aB
#    4. B->aC
#    5. C->a
#    6. C->bS}


map = {'S': [('a', 'A'), ('a', 'B')], 'A': [('b', 'S')], 'B': [
    ('a', 'C')], 'C': [('a', ''), ('b', 'S')]}


def check(word):
    next = 'S'

    for i in range(len(word)):
        keys = []
        for j in range(len(map[next])):
            keys.append(map[next][j][0])

        if word[i] in keys:
            if next == "S":
                if (i + 1 == len(word)):
                    return False
                if word[i + 1] == "b":
                    next = map[next][0][1]
                if word[i + 1] == "a":
                    next = map[next][1][1]

            elif next == "C" and word[i] == "a":
                next = ''
            elif next == "C" and word[i] == "b":
                next = "S"
            else:
                next = map[next][0][1]

            if next == '' and (i + 1 == len(word)):
                return True
            elif next == '':
                return False
        else:
            return False
    return False


while 1:
    string = input("Input: ")
    print(check(string))
