#!/bin/python
import math
import re
import functools

INPUT='day5.input'
#INPUT='day5.small.input'

data = open(INPUT).readlines()

# read rules and updates
rules=[]
updates=[]
for l in (data):
    if '|' in l:
        rules.append([int(i) for i in l.strip().split('|')])
    elif ',' in l:
        updates.append([int(i) for i in l.strip().split(',')])
    else:
        pass

def compare(x,y):
    for r in rules:
        if r[0] == x and r[1] == y:
            return 1
        elif r[1] == x and r[0] == y:
            return -1
    return 0 #no rules match

#part 1 & 2
res1=0
res2=0
for u in updates:
    u_sorted = sorted(u, key=functools.cmp_to_key(compare), reverse=True)

    m = len(u)//2
    if u == u_sorted:
        res1+=u[m]              
    else: #add middle elt to the list if update is kept
        res2+=u_sorted[m]


print(f"[SOLVED] - First star: {res1}")
print(f"[SOLVED] - Second star: {res2}")
