#!/bin/python
import math

INPUT='day2.input'
#INPUT='day2.test.input'

data = open(INPUT).readlines()

list1=[]

for l in data:
    l1 = l.split(' ') 
    list1.append([int(i.strip()) for i in l1])

#part 1
res = 0
c = 0
for la in list1:
    #calc all possible list
    lu=[la]
    for n in range(len(la)):
        li=la.copy()
        del li[n]
        lu.append(li)

    for l in lu:
        i0 = l[0]
        safe = True
        inc=False
        dec=False
        high=False
        for i in l[1:]:
            d = abs(i-i0)
            if d < 1 or d > 3:
                safe=False
                high=True
                break  #unsafe 
            if i > i0:
                if dec:
                    safe=False
                    break #unsafe
                inc = True
            if i < i0:
                if inc:
                    safe=False
                    break #unsafe
                dec = True
            i0 = i

        if safe:
            res+=1 
            break
        
        #print(f"{c} {l} {safe} inc {inc} dec {dec} high {high}")

print(f"[SOLVED] - First star: {res}")

#print(f"[SOLVED] - Second star: {res}")
