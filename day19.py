#!/bin/python
import math
import re
import sys

#INPUT='day19.input'
INPUT='day19.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

data = open(INPUT).readlines()
designs=[]
towel_patterns=data[0].strip().split(', ')
for y, l in enumerate(data):
    if y>1:
        designs.append(l.strip())

print(towel_patterns)
print(designs)

def getpossiblepatternsat(d, i):

    next_idx=[]
    #print(f"Checking at index {i}")
    for t in towel_patterns:
        try:
            if d[i:].startswith(t):
                if i+len(t) == len(d):
                    next_idx.append(len(d))
                    #return []
                else:
                    #keep it for next loop
                    next_idx.append(i+len(t))
        except Exception as e:
            print(f"{e}")

    #print(f"{next_idx}")
    #input()
    return next_idx

def check_design(d):
    #get possible start
    checked_idx={}
    nc=[0]
    c=nc
    l=len(d)
    print(f"Check design {d} len {l}")
    while len(c)>0:
        nc=[]
        for i in c:
            if i not in checked_idx:
                 a=getpossiblepatternsat(d,i)
                 checked_idx[i]=a
                 nc+=a

        c=nc 

    return checked_idx

#part 1 & 2
res1=0
res2=0
#count from 0 to e (len of design)

def count_path(s, t, cp, cp_count):
    if s == t:
        return 1
    elif cp_count[s] != 0:
        return cp_count[s]
    else:
        for c in cp[s]:
            cp_count[s]+= count_path(c,t, cp, cp_count)

    return cp_count[s]

#Calc the 2 stars
for d in designs:
    l=len(d)
    cp=check_design(d)
    print(f"{cp}")

    #part 1
    if l in cp:
        print(f">>> {d} is valid")
        res1+=1

    cp_count={}
    for c in cp:
        if c == l:
            cp_count[c]=1
        else:
            cp_count[c]=0

    a=count_path(0, l, cp, cp_count)
    print(f"Number of path for design {d} is {a}")
    res2+=a
    #part 2
    #init


print(f"[SOLVED] - First star: {res1}")
print(f"[SOLVED] - Second star: {res2}")
