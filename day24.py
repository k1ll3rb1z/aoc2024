#!/bin/python
import math
import re
import sys
import itertools
import functools

#INPUT='day24.input'
INPUT='day24.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

ARG2=0
try:
    ARG2=int(sys.argv[2])
except:
    pass


data = open(INPUT).readlines()
data= [l.strip() for l in data]

wires={}
operations={}
op_func={
    'XOR': lambda x,y: x^y,
    'AND': lambda x,y: x&y,
    'OR': lambda x,y: x|y
}

all_wires=[]

readop=False
for l in data:
    if len(l) == 0:
        readop=True
        continue
    if readop:
        o,w=l.split(' -> ')
        a,o,b=o.split(' ')
        operations[(a,o,b,w)]=0 #not exec
        all_wires.append(a)
        all_wires.append(b)
    else:
        n,v=l.split(': ')
        wires[n]=int(v)
        all_wires.append(n)

all_wires=list(set(all_wires))
l_all_wires=len(all_wires)

print(f"{wires}")
print(f"{all_wires}")
print(f"{operations}")

#solve operations
current_len=len(wires)
while l_all_wires != current_len:
    print(f"{len(wires)}/{l_all_wires}") 
    prev_len=current_len
    for op in operations:
        if operations[op] == 0: #not done
            a,o,b,r=op
            if a in wires and b in wires and r not in wires:
                wires[r] = op_func[o](wires[a],wires[b])
                operations[op] = 1
    
    current_len=len(wires)
    if prev_len == current_len:
        break

#part 1
for w in sorted(wires.keys()):
    print(f"{w}: {wires[w]}")

res=''
for w in sorted(wires.keys()):
    if w[0] == 'z':
        res=str(wires[w])+res

res=int(res,2)     

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
