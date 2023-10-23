def checkbalance(w):
    counter_1=0
    counter_0=0
    w=list(w)
    for i in range(len(w)):
        if w[i]=='(':
            counter_1+=1
        else:
            counter_0+=1
        if (counter_1-counter_0)<0:
            return False
    if counter_1==counter_0:
        return True
    else:
        return False
    
w='()(()())()()'
print(checkbalance(w))
        
#def randombracketgenerator(n):
#    import random
#    w=[]
#    n=2*n
#    for i in range(n):
#        if random.randint(0,1)==1:
#            w.append(1)
#        else:
#            w.append(0)
#    return w

#def test(n):
#    i=1
#    while i<=n:
#        w=randombracketgenerator(i)
#        i+=1
#        if checkbalance(w):
#            print(w,' is balanced')
#        else:
#            print(w,' is not balanced')

