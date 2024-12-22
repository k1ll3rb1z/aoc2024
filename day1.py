#!/bin/python
import math

INPUT='day1.1.input'

data = open(INPUT).readlines()

list1=[]
list2=[]


for l in data:
    l1, l2 = l.split('   ') 
    list1.append(int(l1.strip()))
    list2.append(int(l2.strip()))

list1 = sorted(list1)
list2 = sorted(list2)

#part 1
res = 0
for l1, l2 in zip(list1, list2):
    res+=abs(l2-l1)

print(f"[SOLVED] - First star: {res}")

#part 2
res = 0
for l1 in list1:
   for l2 in list2:
       if l1 == l2:
           res+=l1

print(f"[SOLVED] - Second star: {res}")
