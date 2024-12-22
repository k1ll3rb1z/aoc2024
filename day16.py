#!/bin/python
import math
import re
import sys

INPUT='day16.input'
#INPUT='day16.small.input'
global maze,S,E,visited,scores,dirs,dirs_c,stop,enum_turns,enum_dirs

enum_turns={
    1: 1000,
    0: 0,
    2: 2000,
    3: 1000
}

try:
    INPUT=sys.argv[1]
except:
    pass    

stop=0
try:
    stop=int(sys.argv[2])
except:
    pass


maze = open(INPUT).readlines()
S=[0,0]
E=[0,0]

for y, l in enumerate(maze):
    maze[y]=[c for c in l.strip()]
    for x,c in enumerate(l):
        if c == 'S':
            S=[x,y]
        elif c == 'E':
            E=[x,y] 

xlen=len(maze[0])
ylen=len(maze)


def setat(p,o):
    global maze
    maze[p[1]][p[0]]=o

def getat(p):
    global maze
    return maze[p[1]][p[0]]

#      Left,  up,    righ, down"
dirs=[(-1,0),(0,-1),(1,0),(0,1)]
enum_dirs={
    (-1,0):0,
    (0,-1):1,
    (1,0) :2,
    (0,1) :3
}

dirs_c=['<','^','>','v']
print(f"Maze {xlen}x{ylen} S:{S} to E:{E}")

# visited contained the score
visited_dirs={}
for d in dirs:
    visited_dirs[d]=math.inf

visited=[ [ visited_dirs.copy() for j in range(xlen)] for i in range(ylen) ]

#pos + dir
def setvisited(p, d, score):
    global visited
    visited[p[1]][p[0]][d]=score

#pos + dir
def getvisited(p, d):
    global visited
    return visited[p[1]][p[0]][d]

def draw():
    global maze

    for y,l in enumerate(maze):
        for x, c in enumerate(l):
            sys.stdout.write(c)
        sys.stdout.write('\n')
    sys.stdout.flush()

#Set starting score at 0 for current dir and adjust score for other dirs
setvisited(S,dirs[2],0)
setvisited(S,dirs[3],1000)
setvisited(S,dirs[1],1000)
setvisited(S,dirs[0],2000)
points=[S] #starting east
scores=[]

# calc cells around p
def calcnext(points):
    global visited, maze, scores,dirs,dirs_c,E,stop,enum_turns
    next_p=[] 
    print(f">> calc next of {points}") 
    for p in points:
        print(f"> {p}")
        for i,d in enumerate(dirs):
            np=[p[0]+d[0],p[1]+d[1]]
            o=getat(np)

            if o != '#': #possible path
                score=getvisited(p, d)+1 #get current score for dir
                score_next=getvisited(np, d)

                if score < score_next: 
                    print(f">> adding {np}:{dirs_c[i]} ->{score} (from {score_next})") 
                    next_p.append(np)

                    #set lower score
                    setvisited(np, d, score)
                    #calc other directions
                    if np == E:
                         print(f">>> E discovered adding a new score {score}") 
                         scores.append(score)
                    else: 
                        for i2, d2 in enumerate(dirs):
                            #check if dir goes in a wall
                            np2 = [np[0]+d2[0],np[1]+d2[1]]
                            if np2 != p:
                                iop2 = (i2+2)%4
                                op2 = dirs[iop2]
                                tmp_score=getvisited(np, op2)
                                tmp_score_next=score+enum_turns[abs(iop2-i)]
                                if tmp_score_next < tmp_score:
                                    setvisited(np, op2, tmp_score_next)
                    
                    #if draw requested
                    if stop:
                        setat(np, dirs_c[i])
                        draw()
                        input()
            else:
                setvisited(np, d, math.inf)

    return next_p

while len(points) > 0:
    points=calcnext(points)
      
print(scores)
#part 1
res=0

scores=[]
v=visited[E[1]][E[0]]
for d in dirs:
    scores.append(v[d])
res=sorted(scores)[0]

print(f"[SOLVED] - First star: {res}")
print(f">>>>> E Visited <<<<<<\n{v}")
input()
if stop:
    print(f">>>>> Visited <<<<<<\n{visited}")

#part 2 find all tiles part of a best path
res=1 #E

points=[]
scores=[]
v=visited[E[1]][E[0]]
for d in dirs:
     scores.append(v[d])
     low_s=sorted(scores)[0] #low score

for i,d in enumerate(dirs):
    if v[d] == low_s:
        points.append([E, i, low_s])

good_spots=[]
print(f"Part2: Starting from {points}")
input()
while len(points) != 0:
    scores=[]
    npoints=[]
    for p,i,sc in points:#coordinates + direction
        v=visited[p[1]][p[0]]
        #keep best escore
        
        for i2,d2 in enumerate(dirs):
            delta_score=1
            iop = (i2+2)%4
            delta_score+=enum_turns[abs(iop-i)]

            np = [p[0]+d2[0],p[1]+d2[1]]
            print(f"Checking {np}")
            if getat(np) != '#':
                od = dirs[iop] #opp dir
                nv = visited[np[1]][np[0]]
                print(f"{p} {iop} score:{sc}-{delta_score} -> check {np} {od} {nv[od]} {nv}")

                if nv[od] == sc-delta_score:
                    print(f"Adding {np, iop, nv[od]}")
                    npoints.append([np, iop, nv[od]])
                    good_spots.append((np[0],np[1]))

    print(f"next to visit {npoints}")
    #input()
    points=npoints

for o in good_spots:
    setat(o, 'o')
draw()
res+=len(set(good_spots))
print(f"[SOLVED] - Second star: {res}")
