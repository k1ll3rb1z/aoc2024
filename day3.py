#!/bin/python
import math
import re

INPUT='day3.input'
#INPUT='day2.test.input'

data = open(INPUT).readlines()
mul_re=re.compile(r'mul\([\d]{1,3}\,[\d]{1,3}\)')

res=0
for l in data:
    for n in mul_re.findall(l):
        res += next(map(lambda x,y:x*y, *tuple([[int(i)] for i in n[4:-1].split(',')])))

print(f"[SOLVED] - First star: {res}")
#part 2
mul_re=re.compile(r'(mul\([\d]{1,3}\,[\d]{1,3}\)|do\(\)|don\'t\(\))')
res=0

go=True
for l in data:
    for n in mul_re.findall(l):
        match n:
            case 'do()':
                go=True
            case 'don\'t()':
                go=False
            case _:
                if go:
                    res += next(map(lambda x,y:x*y, *tuple([[int(i)] for i in n[4:-1].split(',')])))
    
print(f"[SOLVED] - Second star: {res}")
