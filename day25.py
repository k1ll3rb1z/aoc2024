#!/bin/python
import math
import re
import sys
import itertools
import functools

#INPUT='day25.input'
INPUT='day25.small.input'

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
data = [l.strip() for l in data]

keys=[]
locks=[]

i=0
ldata=len(data)
while i<ldata:
    l=data[i]
    if l == '.....':
        #key
        key=[0,0,0,0,0]
        for j in range(1,6):
            for e,c in enumerate(data[i+j]): 
                key[e]+=int(data[i+j][e] == '#')
        keys.append(key)

    elif l == '#####':
        #lock
        lock=[0,0,0,0,0]
        for j in range(1,6):
            for e,c in enumerate(data[i+j]): 
                lock[e]+=int(data[i+j][e] == '#')
        locks.append(lock)
    else:
        raise Exception('Bad input')
    
    i+=8

print(f"{keys}")
print(f"{locks}")

#part 1 count keys matching locks
res=0
for l in locks:
    for k in keys:
        match=True
        for i in range(5):
            if k[i]+l[i]>5:
                match=False
                break
        if match:
            res+=1

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
