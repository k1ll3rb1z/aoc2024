#!/bin/python
import math
import re
import sys
import itertools
from functools import lru_cache

#INPUT='day23.input'
INPUT='day23.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

ARG2=2
try:
    ARG2=int(sys.argv[2])
except:
    pass


data = open(INPUT).readlines()
data = [tuple(sorted([i for i in l.strip().split('-')])) for l in data]
print(f"{data}")

set_of_three_computer={}
set_of_computer={}

for i,j in data:
    if i not in set_of_computer:
        set_of_computer[i]=[j]
    else:
        if j not in set_of_computer[i]:
            set_of_computer[i].append(j)

    if j not in set_of_computer:
        set_of_computer[j]=[i]
    else:
        if i not in set_of_computer[j]:
            set_of_computer[j].append(i)

print(f"{set_of_computer}")

#calc set of 3
for c,v in set_of_computer.items():
    for t in itertools.combinations(v, 2):
        r=(c,)+t
        linked=True
        for e in itertools.combinations(t, 2):
            if tuple(sorted(t)) not in data:
                linked=False
                break

        if linked:
            r=tuple(sorted(r))
            if r not in set_of_three_computer:
                chief=False
                for p in r:
                    if p[0]=='t':
                        chief=True
                    
                set_of_three_computer[r]=chief


print(f"{set_of_three_computer}")
#part 1
res=0
count=0
for r in set_of_three_computer:
    count+=1
    if set_of_three_computer[r]:
        res+=1


print(f"[SOLVED] - First star: {res} {count}")

#part 2 find largest netowrk

#check if a computer is part of the network (list of computer)
def check_candidate(e, network):
    for i in network:
        if i not in set_of_computer[e]:
            return False
    network.append(e)
    return True

def calc_next(current_set):
    newset=[]
    for c in current_set:
        for e in set_of_computer:
            adde=True
            for i in c:
                if e != c:
                    if e not in set_of_computer[i]:
                        adde=False
                        break
            if adde:
                newset.append(c+(e,))

    return newset

res=0

#for n in range(len(data)):

networks=[]
for p in data:    
    c1,c2=p
    #check if c1 and c2 not already part of a calulated network
    newnet=True
    for n in networks:
        if c1 in n and c2 in n:
            newnet=False
            break
    if newnet:
        n=[c1,c2]
        print(f"Starting from {n}")
        for i in set_of_computer:
            check_candidate(i,n)
        print(f"Network size is {len(n)}")
        networks.append(n)
        print(f"Network size is {len(n)}")


#current_set=[]
#max_len=2
#for c in set_of_computer:
#    for i in set_of_computer[c]:
#        current_set.append((c,i))
#
#for i in range(ARG2):
#    new_set=calc_next(current_set)
#    if len(new_set)==0:
#        break
#    current_set=new_set
max_len=0
winner=[]

for n in networks:
    l=len(n)
    if l > max_len:
        max_len=l
        winner=n

print(f"[SOLVED] - Second star: {max_len} {','.join(sorted(winner))}")
