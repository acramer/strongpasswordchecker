import re


# aaa111 : 2
# bbaaaaaaaaaaaaaaacccccc : 8
# bbaaaaaaaaaaaaaaaaaacccccc : 11
# FFFFFFFFFFFFFFF11111111111111111111AAA : 23
# ..................!!! : 7
# aaaaabbbb1234567890ABA : 3
# bbaaaaaaaaaaaaaaacccccc : 8
# aaaaaaaAAAAAA6666bbbbaaaaaaABBC : 13

# FFFFFFFFFFFFFFF11111111111111111111AAA : 23
# 15                  20                         3   m 1 s 18 = 19
# FFF FFF FFF FFF FFF 111 111 111 111 111 111 11 AAA : 0
# FFF FFF FFF FFF FF  111 111 111 111 111 111 11 AA  : 2
# s 16
# FF                  111 111 111 111 111 1      AA  : 16
# FF                  141 131 121 1o1 1a1 1      AA  : 5  = 23
#                                                    : 19 + 16//3 - 1  = 23

# ..................!!! : 7
# 18                      3   m 3 s 1 = 4
# ... ... ... ... ... ... !!! : 0
# ... ... ... ... ... ..  !!! : 1
# ..5 ..4 ..3 ..2 ..A ..  a!! : 6 = 7

# aaaaabbbb1234567890ABA : 3
# 5      4     10            3   m 0 s 2 = 2
# aaa aa bbb b 123 456 789 0 ABA : 0
# aaa aa bb    123 456 789 0 ABA : 2
# aa! aa bb    123 456 789 0 ABA : 1 = 3

# bbaaaaaaaaaaaaaaacccccc : 8
# 2  15                  6       m 2 s 3
# bb aaa aaa aaa aaa aaa ccc ccc : 0
# bb aaa aaa aaa aaa aa  ccc cc  : 2
# bb aaa aaa aaa aaa aa  ccc c   : 1
# bb aa4 aa3 aa2 aa1 aa  cAc c   : 5 = 8

# aaaaaaaAAAAAA6666bbbbaaaaaaABBC : 13
# 7         6       4     4     6       4    m 0 s 11
# aaa aaa a AAA AAA 666 6 bbb b aaa aaa ABBC : 0
# aaa aaa a AAA AA  666 6 bbb b aaa aaa ABBC : 1
# aaa aaa a AAA AA  666 6 bbb b aaa aa  ABBC : 2
# aaa aa    AAA AA  666 6 bbb b aaa aa  ABBC : 4
# aaa aa    AAA AA  66    bbb b aaa aa  ABBC : 6
# aaa aa    AAA AA  66    bb    aaa aa  ABBC : 8
# aa        AAA AA  66    bb    aaa aa  ABBC : 11
# aa        AA1 AA  66    bb    aa0 aa  ABBC : 2 = 13



def main():
    tests = [('aaa111',2),
             ('bbaaaaaaaaaaaaaaacccccc',8),
             ('bbaaaaaaaaaaaaaaaaaacccccc',11),
             ('FFFFFFFFFFFFFFF11111111111111111111AAA',23),
             ('..................!!!',7),
             ('aaaaabbbb1234567890ABA',3),
             ('bbaaaaaaaaaaaaaaacccccc',8),
             ('aaaaaaaAAAAAA6666bbbbaaaaaaABBC',13)]
    clean = True
    for t,k in tests:
        a = strongPasswordChecker(t)
        clean *= a==k
        if a != k:
            print('Password:',t,'| Output:',a,'| Expected',k)
    if clean: print('All password tests checkout!')
    while True:
        pw = input('Password Candidate: ')
        if pw == 'q' and input('Do you want to quit? (y/n): ') == 'y': break
        print(strongPasswordChecker(pw))


def strongPasswordChecker(password):
    adds, subs = 0, 0
    if len(password) < 6:    adds = 6 - len(password)
    elif len(password) > 20: subs = len(password) - 20
    addC = max(sum(not bool(re.findall(q,password)) for q in ['[a-z]','[A-Z]','[0-9]'])-adds,0)
    total = adds+subs+addC
    repl = 0

    ccount = 1
    clist = []
    lastc = password[0]
    for i, c in enumerate(password[1:]):
        if c != lastc or i == len(password) - 2:
            if c == lastc: ccount += 1
            if ccount > 2: clist.append(ccount)
            ccount = 1
        else: ccount += 1
        lastc = c

    if subs:
        modlist = sorted([(e%3,i) for i,e in enumerate(clist)],key=lambda x:x[0])
        for mod,edx in modlist:
            if not subs or mod == 2: break
            elem = clist[edx]
            if subs >= mod+1:
                clist[edx] -= (mod+1)
                subs -= (mod+1)
        for edx in range(len(clist)):
            elem = clist[edx]
            if subs:
                if elem < 3: continue
                nelem = max(elem-subs,2) if elem > 2 else elem
                subs = max(subs-(elem-2),0) if elem > 2 else subs
                elem = nelem

            nelem = max(elem-3*addC,0) if elem > 2 else elem
            addC = max(addC-(elem//3),0) if elem > 2 else addC
            elem = nelem

            repl += elem//3

    else:
        for elem in clist:
            nelem = max(elem-2*adds,0)
            adds = max(adds-elem,0) if elem > 2 else adds
            elem = nelem

            nelem = max(elem-3*addC,0)
            addC = max(addC-(elem//3),0) if elem > 2 else addC
            elem = nelem

            repl += elem//3

    return total+repl


if __name__ == '__main__': main()
