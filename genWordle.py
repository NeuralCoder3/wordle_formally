from cgi import print_environ
from z3 import *


WRONG = 0
PRESENT = 1
CORRECT = 2

pairs=[]

with open('test_case.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            continue
        guess, word, result = line.split()  
        pairs.append((guess, word, result))



for g,w,res in pairs:

    k = len(g)

    s = Solver()

    gc=[]
    wc=[]
    fc = []
    mc = []
    for i in range(k):
        gc.append(Int('g'+str(i)))
        wc.append(Int('w'+str(i)))
        fc.append(Int('f'+str(i)))
        mc.append(Int('m'+str(i)))
        
    def Equals(a,b):
        return And(Implies(a,b), Implies(b,a))
        
    s.add(Distinct(mc))
    for i in range(k):
        # restriction on feedback
        s.add(Or(fc[i]==CORRECT, fc[i]==PRESENT, fc[i]==WRONG))
        
        # equal => green and marked
        s.add(Equals(gc[i] == wc[i], fc[i] == CORRECT))
        
        for j in range(k):
            s.add(Implies(mc[j]==i, And(wc[j]==gc[i],Or(fc[i]==CORRECT, fc[i]==PRESENT))))
        
        someMarkedList=[]
        for j in range(k):
            someMarkedList.append(mc[j]==i)
        someMarked=Or(someMarkedList)
        s.add(Implies(Or(fc[i]==CORRECT, fc[i]==PRESENT),someMarked))
        
        s.add(mc[i]<k)
        
        s.add(Implies(
            And(gc[i] != wc[i],
                someMarked),
            fc[i] == PRESENT
        ))
        
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
            allMarkedDiff
        ))
        
        # überflüssig?
        s.add(Implies(Not(charExists), And(fc[i] == WRONG,Not(someMarked))))
        
    
    # to generate words for a feedback
    if False:
        s.add(fc[0] == PRESENT)
        s.add(fc[1] == PRESENT)
        s.add(fc[2] == PRESENT)
        s.add(fc[3] == PRESENT)
        s.add(fc[4] == PRESENT)
        
        s.check()
        m=s.model()
        gs=""
        ws=""
        for i in range(k):
            gs+=chr(m[gc[i]].as_long()+ord('A'))
            ws+=chr(m[wc[i]].as_long()+ord('A'))
        print("g: "+gs)
        print("w: "+ws)
        exit(0)
        
    for i,c in enumerate(g):
        s.add(gc[i] == ord(c))
    for i,c in enumerate(w):
        s.add(wc[i] == ord(c))
        
        
    print("g: ", g)
    print("w: ", w)
    
    s.push()
    # guarantee only one correct solution according to specification
    allSame=[]
    for i,c in enumerate(res):
        v=-1
        if c == "🟩":
            v=CORRECT
        elif c == "🟨":
            v=PRESENT
        elif c == "⬛":
            v=WRONG
        allSame.append(fc[i] == v)
    allSame=And(allSame)
    s.add(Not(allSame))
    if s.check() == sat:
        print("There is a bug in the specification.")
        model = s.model()
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
        exit(1)
    s.pop()    
    
    if s.check() == sat:
        model = s.model()
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
        
            
    print("")