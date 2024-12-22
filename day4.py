#!/bin/python
import math
import re

INPUT='day4.input'
#INPUT='day4.small.input'
#INPUT='day4.small2.input'

data = open(INPUT).readlines()

res=0
#remote line break
for i,l in enumerate(data):
    data[i]=l.strip()

#search for XMAS in all dir
for y, l in enumerate(data):
    for x, c in enumerate(l):
        if c == 'X': #starting point
            #search right, left, etc ...
            dirs=[(1,0),   (-1,0),  (0,1),  (0,-1),  (1,1), (-1,1), (1,-1), (-1,-1)]
            #search all dirs:
            for d in dirs: 
                xd, yd = d
                try:
                    if x+3*xd >=0 and y+3*yd >= 0 and data[y+yd][x+xd] == 'M' and data[y+2*yd][x+2*xd] == 'A' and data[y+3*yd][x+3*xd] == 'S':
                        print(f"XMAS at {x}x{y} dir {xd},{yd}")
                        res+=1
                except:
                    pass

print(f"[SOLVED] - First star: {res}")
res=0
#seach M S
#       A
#      M S
for y, l in enumerate(data):
    for x, c in enumerate(l):
        if c == 'A': #starting point
            if x == 0 or y == 0:
                continue #search right, left, etc ...
            
            #search all dirs:
            try:
                if ((data[y-1][x-1] == 'M' and data[y+1][x+1] == 'S') or \
                    (data[y-1][x-1] == 'S' and data[y+1][x+1] == 'M')) and \
                   ((data[y+1][x-1] == 'M' and data[y-1][x+1] == 'S') or \
                    (data[y+1][x-1] == 'S' and data[y-1][x+1] == 'M')):
                    print(f"X-MAS at {x}x{y}")
                    res+=1
            except:
                pass

#part 2
    
print(f"[SOLVED] - Second star: {res}")
