#!/bin/python
import math
import re

INPUT='day9.input'
#INPUT='day9.small.input'

data = open(INPUT).readlines()[0].strip()

expended=[]
fid=0 #starting file id
for i, l in enumerate(data):
    l=int(l)
    if i%2 == 0: #file id else empty
        for j in range(l):
            expended.append((fid, l))
        fid+=1
    else:
        for j in range(l):
            expended.append((-1,l))

#print(f"Expended {expended}")

#compress
#part 1
res=0
compressed=expended.copy()
i = len(compressed)-1 #last itemp

#print(f"{compressed}\n####")
print(f"Phase compressing in progress")
j = 0
while i > 0:
    c,l = compressed[i]
    if j >= i:
        break

    if c != -1:
        while j < i:
            c2, l2 = compressed[j]
            if c2 == -1: # empty space
                if l2 >= l:
                    for k in range(l):
                        compressed[j+k]=compressed[i-k]
                        compressed[i-k]=(-1,l)

                    for k in range(l2-l):
                        compressed[j+l+k]=(-1,l2-l)

                    i-=l
                    break

                else:
                    for k in range(l2):
                        compressed[j+k]=compressed[i-k]
                        compressed[i-k]=(-1,l)

                    for k in range(l-l2): #reduce lenght of unmoved c
                        compressed[i-l2-k]=(c,l-l2)

                    i-=l2 
                    l-=l2 #adapt l for next step
            j+=l2
    else: #c is -1, pass it
       i-=l



#checksum
i=0
print(f">>> Calculate checksum")
while i < len(compressed):
    fid, s = compressed[i]
    if fid != -1:
        res+=fid*i
    i+=1

#print(f"Compressed {compressed}")
print(f"[SOLVED] - First star: {res}")

#part 2

#compress
res=0
compressed=expended.copy()

#print(f">>> Compressed {compressed}")
i = len(compressed)-1 #last itemp
print(f">>> checking filesystem of len {len(compressed)} starting at {i}")

while i > 0:
    c,l = compressed[i]
    if c != -1:
        j = 0
        while j < i:
            c2, l2 = compressed[j]
            if c2 == -1 and l2>=l: #enought empty space
                #print(f"move {c} from {i} to {j}")
                for k in range(l):
                    compressed[i-l+k+1]=(-1,l)
                    compressed[j+k]=(c,l)

                for k in range(l2-l):
                    compressed[j+l+k]=(-1,l2-l)
                break
            j+=l2

    i-=l    
    

#checksum
i=0
print(f">>> Calculate checksum")
while i < len(compressed):
    fid, s = compressed[i]
    if fid != -1:
       for j in range(s): 
            res+=fid*(i+j)
    i+=s
    
print(f"[SOLVED] - Second star: {res}")
