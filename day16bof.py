#!/bin/python
import math
import re
import sys

#INPUT='day16.input'
INPUT='day16.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass    


global maze,S,E
maze = open(INPUT).readlines()
S=[0,0]
E=[0,0]

for y, l in enumerate(maze):
    maze[y]=maze[y].strip()

xlen=len(maze[0])
ylen=len(maze)

     #  Left, up,    righ, down"
dirs=[(-1,0),(0,-1),(1,0),(0,1)]

def draw(m=None, visited=None):
    global maze,S,E
    if m is None:
        m=maze
    if visited is not None:
        p=visited[0]
        print(f"Current pos is at {p[0]} with dir {p[1]}")
    for y, l in enumerate(m):
        for x, c in enumerate(l):
            if c == 'S':
                S=[[x,y], 2] #pos + dir index, starting at East
            elif c == 'E':
                E=[x,y]
            if visited is not None:
                if getvisited(visited,[x,y]):
                    c = 'o'    
            sys.stdout.write(c)
        sys.stdout.write('\n')
        sys.stdout.flush()

draw()

print(f"S:{S} to E:{E}")

#init paths is one path with all 0
# each path is a pos + the visited array

#p is [(x,y), dir] dir is one of the dirs

def setvisited(path, p):
    path[1][p[1]][p[0]][0]=1

def getvisited(path, p):
    #print(f">>>Get visited {path}")
    #print(f"get visited at {p}")
    return path[1][p[1]][p[0]][0]

def updatescore(path, p, score):
    path[1][p[1]][p[0]][1]+=score  

def getscore(path, p):
    #print(f">>>Get score {path}")
    #print(f"get score at {p}")
    return path[1][p[1]][p[0]][1]

def getroom(p, m=None):
    global maze
    if m is None:
        m=maze
    #print(f"Get room at {p}")
    return m[p[1]][p[0]] 

def getpathcopy(p):
    #print(f">>>Get copy of {p}")
    np=[]
    np.append(p[0].copy())
    np.append([ [j.copy() for j in i] for i in p[1]])
    #print(f">>> Copy is {np}")
    return np

# on visited for each path
visited=[[ [0,0] for j in range(xlen)] for i in range(ylen)]
paths=[ [S, visited] ]

#print(f"paths {paths}")

setvisited(paths[0], S[0])

print(f"paths {paths}")


#optimize paths by only keeping shortest
def removetoolong(paths):
    keep=[]
    for i,p in enumerate(paths):
        keepit=True
        if keepit:
            for x,l in enumerate(p[1]):
                if keepit:
                    for y, c in enumerate(l):
                        v,sc=c
                        if v:
                            for i2,p2 in enumerate(paths):
                                print(f"Comparing {p} and {p2}")
                                if i!=i2:
                                    sc2 = getscore(p2, [x,y])
                                    if sc2 < sc:
                                        print(f"Removing a too long path {sc2} vs {sc} at {[x,y]}, visited {v}")
                                        keepit=False
                                        break
        if(keepit):
            keep.append(p)
               
    return keep
    

#return list of maze from a list of maze and update visited
def getnextpaths(paths):
    newpaths=[]
    for pi, p in enumerate(paths):
        s,sd=p[0] #pos and dir index
        v=p[1] #visited array
        #print(f"Check around {s} dir {sd}:{dirs[sd]}")
        
        #get next available pos
        for i, d in enumerate(dirs):
            np=[s[0]+d[0],s[1]+d[1]]
            #print(f"Check pos {np} for dir {d}")

            o = getroom(np)

            if o == '#': #not interresting
                #print(f"wall {o} at {np}")
                pass
            elif getvisited(p, np) == 0:
                #print(f"{np}:'{o}' not visited")
                #copy p
                p_copy=getpathcopy(p)
                #update score base on turn
                p_copy[0]=[np, i] #udpate path current pos
                new_score=getscore(p_copy, s)+1+(abs(sd-i)%4)*1000
                updatescore(p_copy, np, new_score)

                setvisited(p_copy, np)
                
                #draw(visited=p_copy)
                #input()
                if o == 'E':
                    print(f"End detected at {np} with a score of {getscore(p_copy,np)}")
                    #input()

                #check other scores
                keep = True
                for p2i, p2 in enumerate(paths):
                    if p2i != pi:
                        sc2 = getscore(p2, np)
                        v = getvisited(p2, np)
                        if v and (sc2 < new_score):
                            print(f"Path too long {np}:{new_score} vs {sc2}, not keeping")
                            keep = False
                            break
                if keep:
                    newpaths.append(p_copy)

    #print(f"Returning {len(newpaths)} new paths")
    #newpaths=removetoolong(newpaths)
    print(f">> after optim {len(newpaths)} new paths")
    return newpaths


def calcallpaths(paths):
    scores=[]
    while len(paths) >0: 
        for p in paths:
            s,d=p[0]
            if s == E:
                score = getscore(p, s)
                print(f"E reached with a score of {score}")
                draw(visited=p)
                scores.append(score)

        paths=getnextpaths(paths)
    return scores 

scores=calcallpaths(paths)
print(scores)
#part 1
res=0
#for y, l in enumerate(data):
res=sorted(scores)[0]
print(f"[SOLVED] - First star: {res}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")
