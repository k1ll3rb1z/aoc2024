#!/bin/python
import math
import re
import sys
import time

#INPUT='day18.input'
INPUT='day18.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

if INPUT == 'day18.small.input':
    size=7  #small example
    falling_num=12
else:
    size=71 #big example
    falling_num=1024

#coord max for x and y
cmax=size-1

data = open(INPUT).readlines()
incoming_pos=[[int(i) for i in l.strip().split(',')] for l in data]

print(f"{incoming_pos}")

def draw(m):
    for y,l in enumerate(memory):
        for x, c in enumerate(l):
            sys.stdout.write(c)
        sys.stdout.write('\n')
    sys.stdout.flush()

def calcmemory(falling_num):
    memory=[['.' for i in range(size)] for j in range(size)]
    #draw(memory)
    for y,l in enumerate(memory):
        for x,c in enumerate(l):
            print(f"{[x,y]}")
            if [x,y] in incoming_pos[:falling_num]:
                memory[y][x]='#' 
    
            if [x,y] == [0,0]:
                memory[y][x]='S' 
            
            if [x,y] == [cmax,cmax]:
                memory[y][x]='E' 
            #draw(memory)
            #input()
    return memory 
#print(f"{memory}")

def updatememory(memory, f):
    x,y=incoming_pos[f]
    memory[y][x]='#'
    return memory

memory=calcmemory(falling_num)

draw(memory)

# scores for the dijkstra algo
def calcpath(memory):
    dirs=[(0,1),(1,0),(-1,0),(0,-1)]
    scores=[[math.inf for i in range(size)] for j in range(size)]
    scores[0][0]=0 #init score is 0
    c=[[0,0]]
    scores_at_arrival=[]
    while(len(c)>0):
        new_c=[]
        for p in c:
            x,y=p
            s=scores[y][x]
            for d in dirs:
                nx = p[0]+d[0]
                ny = p[1]+d[1]
                if nx>=0 and nx<=cmax and ny>=0 and ny<=cmax:
                    np=[nx, ny]
                    if memory[ny][nx] != '#':
                        if s+1 < scores[ny][nx]:
                            scores[ny][nx]=s+1
                            if np!=[cmax,cmax]:
                                new_c.append(np)
                                
                                #for debug
                                #memory[ny][nx]='O'
                                #draw(memory)
                                #time.sleep(0.0001)
                                #input()
                            else:
                                scores_at_arrival.append(s+1)
        c=new_c
    return scores_at_arrival
        
results=calcpath(memory)

print(f"{results}")
#part 1
res=sorted(results)[0]
#for y, l in enumerate(data):

print(f"[SOLVED] - First star: {res}")

#part 2
res=0
f=falling_num-1

while(len(results)>0):
    f+=1
    memory=updatememory(memory,f)
    results=calcpath(memory)
    
print(f"[SOLVED] - Second star: {incoming_pos[f]}")

