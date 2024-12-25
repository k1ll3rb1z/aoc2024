#!/bin/python
import math
import re
import sys
import itertools
import functools

#INPUT='day23.input'
INPUT='day23.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

ARG2=0
try ARG2:
    ARG2=int(sys.argv[2])
except:
    pass


data = open(INPUT).readlines()
data = [l.strip() for l in data]



#part 1
res=0

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
