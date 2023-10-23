def balancedsubsequence(a):
    a=list(a)
    count=0
    max=0
    j=0
    k=len(a)-1
    i=0
    while i<=len(a)-1:
        if a[i]=='(':
            count+=1
        else:
            count-=1
        length=i-j+1
        if count==0 and length>max:
            max=length 
        if count<0:
            count=0
            length=i-j
            j=j+1
            if length>max:
                max=length
        i+=1
    count=0
    j=len(a)-1
    while j>=0:
        if a[j]=='(':
            count+=1
        else:
            count-=1
        length=k-j+1
        if count==0 and length>max:
            max=length
        if count>0:
            count=0
            length=k-j
            k=k-1
            if length>max:
                max=length
        j-=1
    return max

a='((())('
print(balancedsubsequence(a))