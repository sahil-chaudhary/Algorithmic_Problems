def findingelements(A):
    """The function returns n elements such that their sum is a multiple of n and left over elements if len(A)=2n-1"""
    #This only works if n=2^k
    Result = []
    leftover=[]
    A_1=[]
    A_2=[]
    A_3=[]
    B_1=[]
    if len(A)==3:
        if (A[1]+A[2])%2==0:
            Result.append(A[1])
            Result.append(A[2])
            leftover.append(A[0])
            return [Result,leftover]
        elif (A[0]+A[1])%2==0:
            Result.append(A[0])
            Result.append(A[1])
            leftover.append(A[2])
            return [Result,leftover]
        else:
            Result.append(A[0])
            Result.append(A[2])
            leftover.append(A[1])
            return [Result,leftover]
    else:
        len1=int((len(A)-1)/2)
        i=0
        while i<=len1-1:
            A_1.append(A[i])
            i+=1
        i=len1
        while i<=len(A)-2:
            A_2.append(A[i])
            i+=1
        A_3.append(A[len(A)-1])
        O_1=findingelements(A_1)
        O_2=findingelements(A_2)
        i=0
        a=0
        while i<=len(O_1[0])-1:
            a+=O_1[0][i]
            i+=1
        i=0
        b=0
        while i<=len(O_2[0])-1:
            b+=O_2[0][i]
            i+=1
        a=int(a/(len(O_1[0])))
        b=int(b/(len(O_2[0])))
        if (a+b)%2==0:
            for i in range(0,len(O_1[0])):
                Result.append(O_1[0][i])
                Result.append(O_2[0][i])
            for i in range(0,len(O_1[1])):
                leftover.append(O_1[1][i])
                leftover.append(O_2[1][i])
            leftover.append(A_3[0])
        else:
            for i in range(0,len(O_1[1])):
                B_1.append(O_1[1][i])
                B_1.append(O_2[1][i])
            B_1.append(A_3[0])
            O_3=findingelements(B_1)
            i=0
            while i<=len(O_3[1])-1:
                leftover.append(O_3[1][i])
                i+=1
            i=0
            c=0
            while i<=len(O_3[0])-1:
                c+=O_3[0][i]
                i+=1
            c=int(c/(len(O_3[0])))
            if (a+c)%2==0:
                for i in range(0,len(O_1[0])):
                    Result.append(O_1[0][i])
                    Result.append(O_3[0][i])
                    leftover.append(O_2[0][i])
            else:
                for i in range(0,len(O_1[0])):
                    Result.append(O_2[0][i])
                    Result.append(O_3[0][i])
                    leftover.append(O_1[0][i])
        return [Result,leftover]
import random    
def randomlist(k):
    """The function returns a list of random (2^k-1) integers"""
    len1=2**k-1
    i=0
    A=[]
    while i<=len1-1:
        A.append(random.randint(0,20))
        i+=1
    return A

def test(x):
    """The function tests the function findingelements"""
    A=randomlist(x)
    B=findingelements(A)
    sum=0
    for i in range(0,len(B[0])):
        sum+=B[0][i]
    n=int(len(B[0]))
    if sum%n==0:
        assert True
    else:
        print(False)

i=0
x=3
while x<=20:
    while i<=10:
        test(x)
        i+=1
    x+=1
    i=0