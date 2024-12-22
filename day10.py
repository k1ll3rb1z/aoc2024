#!/bin/python
import math
import re

INPUT='day10.input'
#INPUT='day10.small.input'

global x_max, y_max, hicking_map

hicking_map = open(INPUT).readlines()

trailhead_starts=[]

y_max=len(hicking_map)-1
x_max=0
for y, l in enumerate(hicking_map):
    hicking_map[y]=l=[int(i) for i in l.strip()]
    x_max=len(l)-1
    for x, h in enumerate(l):
        if h == 0:
            s = (x,y)
            print(f"start at {s})")
            trailhead_starts.append(s) 

print(f"map {hicking_map})")
print(f"tail {trailhead_starts})")

#part 1
def geth(s):
    global hicking_map
    return hicking_map[s[1]][s[0]]

def nextdir(s, d):
    global x_max, ymax
    x,y=s
    nx=x+d[0]
    ny=y+d[1]
    if nx < 0 or nx > x_max or ny < 0 or ny > y_max:
        return None
    else:
        return (nx, ny)    
# parse map from all starts
# right, left, up, down
dirs = [(1,0),(-1,0),(0,-1),(0,1)]

#get valid next points from a point (s is the start)
def findnextgoodpoint(p, s):
    npoints=[]
    h = geth(p)
    summits=[]
    for d in dirs:
        snext = nextdir(p, d)
        #print(f"from {s} next is {snext} for dir {d})")
        if snext is not None: #still un the map
            hn = geth(snext)
            #print(f"prev vs new height {h} {hn}")
            if (hn-h)==1:
                #print(f">> good path {snext} with height {hn}")
                if hn == 9: #endpoint reached
                    #print(f">> summit reached at {snext}")
                    summits.append((snext,s))
                else:
                    #print(f">> keep for next search {npoints}")
                    npoints.append(snext)
    for o in npoints:
        summits+=findnextgoodpoint(o, s)

    return summits

res=[]
for s in trailhead_starts:
   res+=findnextgoodpoint(s,s)

res=len(set(res))


print(f"[SOLVED] - First star: {res}")

#part 2
res=0
for s in trailhead_starts:
   res+=len(findnextgoodpoint(s,s))

print(f"[SOLVED] - Second star: {res}")
