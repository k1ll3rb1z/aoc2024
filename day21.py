#!/bin/python
import math
import re
import sys
import itertools
from functools import lru_cache

#INPUT='day21.input'
INPUT='day21.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

DEPTH=2
try:
    DEPTH=int(sys.argv[2])
except:
    pass

codes = open(INPUT).readlines()

codes = [l.strip() for l in codes]

num_keypad=[['7','8','9'],
            ['4','5','6'],
            ['1','2','3'],
            ['#','0','A']]
num_keypad_coord={
    '7':[0,0],
    '8':[1,0],
    '9':[2,0],
    '4':[0,1],
    '5':[1,1],
    '6':[2,1],
    '1':[0,2],
    '2':[1,2],
    '3':[2,2],
    '#':[0,3],
    '0':[1,3],
    'A':[2,3]

}



dir_keypad=[['#','^','A'],
            ['<','v','>']]
dir_keypad_coord={
    '#':[0,0],
    '^':[1,0],
    'A':[2,0],
    '<':[0,1],
    'v':[1,1],
    '>':[2,1]
}

     # ^       <     v     >
DIRS=[(0,-1),(-1,0),(0,1),(1,0)]
DIRS_char={
    (0,-1):'^',
    (-1,0):'<',
    (0,1):'v',
    (1,0):'>'
}

#num key pad calculation
#calc all shortest sequence from A to a number and from a number to A
#contains the list of possible shortest path
shortest_num_keypad={}
#init
xmax_nk=2
ymax_nk=3

#calc shortest path
for a,b in itertools.product('0123456789A', repeat=2):
    visited=[[math.inf for i in range(xmax_nk+1)] for i in range(ymax_nk+1)]
    S=[num_keypad_coord[a],'']
    sx,sy=S[0]
    visited[sy][sx]=0
    E=[num_keypad_coord[b],'']
    if S[0] == E[0]:
        shortest_num_keypad[a+b]=['A'] #just push A if same key
        #print(f"from {a}:{S} to {b}:{E} needs {0} moves {'A'}")
        continue
    else:
        shortest_num_keypad[a+b]=[] 

    nc=[S]
    print(f"Compute from {a}:{S} to {b}:{E}")
    while len(nc)>0:
        #print(f"{nc}")
        #input()
        new_nc=[]
        for c in nc:
            x,y=c[0]
            s=visited[y][x]
            for d in DIRS:
                vx,vy=d
                nx=x+vx
                ny=y+vy
                if nx>=0 and nx<=xmax_nk and ny>=0 and ny<=ymax_nk:
                    if num_keypad[ny][nx] != '#':
                        if visited[ny][nx] >= s+1:
                             visited[ny][nx] = s+1
                             if [nx,ny] != E[0]:
                                 new_nc.append([[nx,ny], c[1]+DIRS_char[d]])
                             else:
                                 E[1]=c[1]+DIRS_char[d]
                                 print(f"{E} found set path to {E[1]}")
                                 shortest_num_keypad[a+b].append(c[1]+DIRS_char[d]+'A')
        nc=new_nc

    x,y=E[0]
    res=visited[y][x]
    print(f"from {a}:{S} to {b}:{E} needs {res} moves {shortest_num_keypad[a+b]}")

print(f"{shortest_num_keypad}")

#dir key pad calculation
#calc all shortest sequence from A to a number and from a number to A
shortest_dir_keypad={}
#init
xmax_dk=2
ymax_dk=1

#calc shortest path
for a,b in itertools.product('<^>vA', repeat=2):
    visited=[[math.inf for i in range(xmax_dk+1)] for i in range(ymax_dk+1)]
    S=[dir_keypad_coord[a],'']
    sx,sy=S[0]
    visited[sy][sx]=0
    E=[dir_keypad_coord[b],'']
    if S[0] == E[0]:
        shortest_dir_keypad[a+b]=['A']
        print(f"from {a}:{S} to {b}:{E} needs {0} moves {'A'}")
        continue
    else:
        shortest_dir_keypad[a+b]=[] 
    nc=[S]
    print(f"Compute from {a}:{S} to {b}:{E}")
    while len(nc)>0:
        #print(f"{nc}")
        #input()
        new_nc=[]
        for c in nc:
            x,y=c[0]
            s=visited[y][x]
            for d in DIRS:
                vx,vy=d
                nx=x+vx
                ny=y+vy
                if nx>=0 and nx<=xmax_dk and ny>=0 and ny<=ymax_dk:
                    if dir_keypad[ny][nx] != '#':
                        if visited[ny][nx] >= s+1:
                             visited[ny][nx] = s+1
                             if [nx,ny] != E[0]:
                                 new_nc.append([[nx,ny], c[1]+DIRS_char[d]])
                             else:
                                 E[1]=c[1]+DIRS_char[d]
                                 #print(f"{E} found set path to {E[1]}")
                                 shortest_dir_keypad[a+b].append(c[1]+DIRS_char[d]+'A')
        nc=new_nc

    x,y=E[0]
    res=visited[y][x]

#optim pad func
def optim_pad(pad):
    for p in pad:
        char_count={}
        c_max=0
        for r in pad[p]:
            char_count[r]=0
            l=len(r)
            for i,c in enumerate(r):
                if i<l-1: 
                    if c == r[i+1]:
                        char_count[r]+=1
                        if char_count[r] > c_max:
                            c_max=char_count[r]
        pad[p]=[]
        for r in char_count:
            if char_count[r] == c_max:
                pad[p].append(r) 
    
    return pad 

print(f"shortest_num_keypad")
print(f"{shortest_num_keypad}")
#optim shortest
#shortest_num_keypad=optim_pad(shortest_num_keypad)
#
#print(f"optim shortest_num_keypad")
#print(f"{shortest_num_keypad}")

print(f"shortest_dir_keypad")
print(f"{shortest_dir_keypad}")
#shortest_dir_keypad=optim_pad(shortest_dir_keypad)
#
#print(f"optim shortest_dir_keypad")
#print(f"{shortest_dir_keypad}")

def optim_res(codes):
    char_count={}
    c_max=0
    for r in codes: 
        char_count[r]=0
        l=len(r)
        for i,c in enumerate(r):
            if i<l-1: 
                if c == r[i+1]:
                    char_count[r]+=1
                    if char_count[r] > c_max:
                        c_max=char_count[r]
        codes=[] 
        for r in char_count:
            if char_count[r] == c_max:
                codes.append(r) 
        
    return codes


#on the dir keyboard calc score at depth between 2 points
@lru_cache(maxsize=None)
def calc_atob_keyboard(a,b,depth):
    if depth==1:
        score=min([len(j) for j in shortest_dir_keypad[a+b]])
        print(f"{a} to {b} depth:{depth} score:{score}")
        return score

    else:
        scores=[]
        for r in shortest_dir_keypad[a+b]:
            score=0
            r='A'+r
            l=len(r)
            for i in range(l-1):
                score+=calc_atob_keyboard(r[i], r[i+1], depth-1)
            scores.append(score)
        print(f"{a} to {b} depth:{depth} score:{min(scores)}")
        return min(scores)


#part 1
res=0
for c in codes:
    print(c)
    r1=['']
    c='A'+c
    #print(f"Testing {cn}")
    for i in range(len(c)-1):
        t=shortest_num_keypad[c[i]+c[i+1]]
        r1x=[]
        for r in r1:    
            for p in t:
                r1x.append(r+p)
        r1=r1x


    scores=[]
    for r in r1:
        r='A'+r
        l=len(r)
        print(f"{c}: {l} {r}")
        score=0
        for i in range(l-1):
            score+=calc_atob_keyboard(r[i],r[i+1],DEPTH)
        scores.append(score)
    score=min(scores)
    print(f"{c}: {score} {scores}")
    
    res+=int(c[1:-1])*score

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
