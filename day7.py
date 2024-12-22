#!/bin/python
import math
import re
import itertools

INPUT='day7.input'
#INPUT='day7.small.input'

data = open(INPUT).readlines()

#part 1
res=0
for l in (data):
   r, exp = l.strip().split(': ')
   r=int(r)
   #count ' ' in exp
   op_count=exp.count(' ')
   numbers=[int(i) for i in exp.split(' ')]
#   print(f"Working on {exp} with {numbers}")

   #generate all combination of '+' and '*' to replace ' '
   for c in itertools.product('*+|', repeat=op_count):
        calc=numbers[0]
        for i, op in enumerate(c):
            if op == '*':
                calc*=numbers[i+1]
            elif op == '+':
                calc+=numbers[i+1]
            else: #concat
                calc=int(str(calc)+str(numbers[i+1]))

#        print(f"Testing if {exp} with {c} match {r}")
        if  calc == r:
            print(f">>>> Match with {c}")
            res+=r
            break

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
