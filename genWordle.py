from cgi import print_environ
from z3 import *


WRONG = 0
PRESENT = 1
CORRECT = 2


pairs=[]
# prase test_case.txt
# the format is like:
# guess word result

with open('test_case.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            continue
        guess, word, result = line.split()  
        pairs.append((guess, word, result))



# Warning: This formulation is not symmetric.

for g,w,res in pairs:

    k = len(g)

    s = Solver()

    gc=[]
    for i,c in enumerate(g):
        v = Int('g'+str(i))
        s.add(v == ord(c))
        gc.append(v)
        
    wc=[]
    for i,c in enumerate(w):
        v = Int('w'+str(i))
        s.add(v == ord(c))
        wc.append(v)
        
    fc = []
    mc = []
    for i in range(k):
        fc.append(Int('f'+str(i)))
        mc.append(Int('m'+str(i)))
        
    def Equals(a,b):
        return And(Implies(a,b), Implies(b,a))
        
    s.add(Distinct(mc))
    for i in range(k):
        # restriction on feedback
        s.add(Or(fc[i]==CORRECT, fc[i]==PRESENT, fc[i]==WRONG))
        
        # equal => green and marked
        # s.add(Equals(gc[i] == wc[i], And(mc[i] == i, fc[i] == CORRECT)))
        s.add(Equals(gc[i] == wc[i], fc[i] == CORRECT))
        # s.add(Equals(gc[i] == wc[i], mc[i] == i)) # subsumed
        
        for j in range(k):
            s.add(Implies(mc[j]==i, And(wc[j]==gc[i],Or(fc[i]==CORRECT, fc[i]==PRESENT))))
        
        someMarkedList=[]
        for j in range(k):
            someMarkedList.append(mc[j]==i)
        someMarked=Or(someMarkedList)
        s.add(Implies(Or(fc[i]==CORRECT, fc[i]==PRESENT),someMarked))
        
        s.add(mc[i]<k)
        
        # exFormI = []
        # for j in range(k):
        #     exFormI.append(And(gc[i] == wc[j], mc[j] != i))
        smallerUnmarkedList = []
        for i2 in range(k):
            if i2>=i:
                break
            aux = []
            for l in range(k):
                aux.append(mc[l]==i2)
            smallerUnmarkedList.append(And(gc[i] == gc[i2], 
                                Not(Or(aux))))
        noSmallerUnmarked = Not(Or(smallerUnmarkedList))
            
        # not equal =>
        #   (I) if exists the letter in the word 
        #   and it is not marked
        #  (II) and no equal letter before in g is unmarked
        # s.append(Equals(
        #     And(gc[i] != wc[i], 
        #         Or(exFormI),
        #         Not(Or(exFormII))
        #     ),
        #     fc[i] == PRESENT
        # ))
        
        s.add(Implies(
            And(gc[i] != wc[i],
                someMarked),
            fc[i] == PRESENT
        ))
        
        s.add(Implies(
            fc[i] == PRESENT,
            And(someMarked,
                noSmallerUnmarked
            )
        ))
        
        charExists = []
        for j in range(k):
            charExists.append(gc[i] == wc[j])
        charExists=Or(charExists)
        
        allMarkedDiff=[]
        for j in range(k):
            allMarkedDiff.append(Implies(gc[i] == wc[j], And(mc[j]>=0,mc[j] != i)))
        allMarkedDiff=And(allMarkedDiff)
        
        s.add(Implies(
            fc[i]==WRONG,
            # Or(
                # Not(charExists),
                allMarkedDiff
            # )
        ))
        
        
        
        # s.add(Implies(gc[i] != wc[i], 
        #     Implies(And(
        #         Or(exFormI), 
        #         Not(Or(exFormII))),
        #     fc[i] == PRESENT)))
        
        # überflüssig?
        s.add(Implies(Not(charExists), And(fc[i] == WRONG,Not(someMarked))))
        
    print("g: ", g)
    print("w: ", w)
    if s.check() == sat:
        model = s.model()
        # print(model)
        fs=""
        for f in fc:
            if model[f] == CORRECT:
                fs+="🟩"
            elif model[f] == PRESENT:
                fs+="🟨"
            elif model[f] == WRONG:
                fs+="⬛"
            else:
                fs+="⬜"
        print("got     : ",fs)
        print("expected: ", res)
        if fs!=res:
            print("wrong result")
            exit(1)
        # ms=""
        # for i,m in enumerate(mc):
        #     if model[m].as_long()>0:
        #         ms+=str(model[m])
        #     else:
        #         ms+="_"
        #     ms+=" "
        # print(ms)
    print("")