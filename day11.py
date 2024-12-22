#!/bin/python
import math
import re
import sys

INPUT='day11.input'
#INPUT='day11.small.input'

stones={} #stone id and how much
data = [int(i) for i in open(INPUT).readlines()[0].strip().split(' ')]
#data=[125,17]

for s in data:
    if s in stones:
        stones[s]+=1
    else:
        stones[s]=1

print(f"Stones: {stones}")


# find list of stones n in stones
j=0

count=75
res1=0
for i in range(count):
    n_stones={}
    for s in stones:
        if s == 0:
            if 1 in n_stones:
                n_stones[1]+=stones[s]
            else:
                n_stones[1]=stones[s]

        else:
            s_s=str(s)
            l = len(s_s)
            if (l % 2) == 0:
                n = int(s_s[:l//2])
                if n in n_stones:
                    n_stones[n]+=stones[s]
                else:
                    n_stones[n]=stones[s]

                n = int(s_s[l//2:])
                if n in n_stones:
                    n_stones[n]+=stones[s]
                else:
                    n_stones[n]=stones[s]

            else:
                if s*2024 in n_stones:
                    n_stones[s*2024]+=stones[s]
                else:
                    n_stones[s*2024]=stones[s]

    stones=n_stones.copy()
    #part 1
    if i == 24:
        for s in stones:
            res1+=stones[s]

res2=0
for s in stones:
    res2+=stones[s]

print(f"[SOLVED] - First star: {res1}")
print(f"[SOLVED] - Second star: {res2}")
