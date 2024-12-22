#!/bin/python
import math
import re
import sys

#INPUT='day22.input'
INPUT='day22.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

DEPTH=2000
try:
    DEPTH=int(sys.argv[2])
except:
    pass

data = open(INPUT).readlines()
secrets={}
secrets_price_evo={}
secrets_price={}
secrets_price_seq={}

for l in data:
    c=int(l.strip())
    secrets[c]=c
    secrets_price_evo[c]=[]
    secrets_price[c]=[]
    secrets_price_seq[c]={}

def mix(s,s1):
    return s^s1

def prune(s):
    return s%16777216 

def nextsecret(s):
    s1=s

    s=s1*64
    s1=mix(s,s1)
    s1=prune(s1)

    s=s1//32
    s1=mix(s,s1)
    s1=prune(s1)
    
    s=2048*s1
    s1=mix(s1,s)
    s1=prune(s1)
    return s1

#part 1
res=0
for s in secrets:
    s1=s
    pp=int(str(s1)[-1])
    #print(f"pp {pp}")
    for i in range(DEPTH):
        s1=nextsecret(s1)
        np=int(str(s1)[-1])
        #print(f"np {np}")
        secrets_price_evo[s].append(np-pp)
        secrets_price[s].append(np)
        pp=np

    res+=s1
    secrets[s]=s1

print(f"[SOLVED] - First star: {res}")

#calc sequences
for s in secrets:
    e=secrets_price_evo[s]
    p=secrets_price[s]
    for i in range(len(e)-3):
        seq=(e[i], e[i+1], e[i+2], e[i+3])
        if seq not in secrets_price_seq[s]: 
            secrets_price_seq[s][(e[i], e[i+1], e[i+2], e[i+3])]=p[i+3]

#print(secrets)
#print(secrets_price_evo)
allseq=[]
for s in secrets:
    e = secrets_price_seq[s]
    allseq=list(set(allseq+list(e.keys())))
    print(f"Adding {len(e)} to all seq, growing to {len(allseq)} sequences")

maxprice=0
bestseq=None
l=len(allseq)
for j,i in enumerate(allseq):
    price=0
    for s in secrets:
        if i in secrets_price_seq[s]:
            price+=secrets_price_seq[s][i]

    if price>=maxprice:
        print(f"Seq {j+1}/{l}:{i} {price}")
        maxprice=price
        bestseq=i


print(f"[SOLVED] - Second star: {maxprice} for seq {bestseq}")

