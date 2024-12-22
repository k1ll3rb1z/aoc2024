#!/bin/python
import math
import re
import sys

#INPUT='day20.input'
INPUT='day20.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

DIRS=[(1,0),(0,1),(-1,0),(0,-1)]
S=[0,0]
E=[0,0]

race = open(INPUT).readlines()
for y, l in enumerate(race):
    for x, c in enumerate(l.strip()):
        if c == 'E':
            E=[x,y]
        if c == 'S':
            S=[x,y] 
        
        race[y]=[i for i in l.strip()]

ylen=len(race)
xlen=len(race[0])

def draw(r):
    for y, l in enumerate(r):
        for x, c in enumerate(l):
            sys.stdout.write(c)
        sys.stdout.write('\n')
    sys.stdout.flush()

draw(race)
#part 1
res=0

#a cheat c is 3 points first is a wall, the second must be in the track
def validate_cheat(c, cheats, visited,r,d,di):
    x2,y2=c[1]

    if x2>0 and x2<xlen-1 and y2>0 and y2<ylen-1:
        if r[y2][x2] != '#' and visited[y2][x2] == math.inf:#should reach an unvisited point
            return True
        #if r[y2][x2] == '#':
        #    for i in range(4):
        #        if i != di:
        #            n1x=x2+DIRS[i][0]
        #            n1y=y2+DIRS[i][1]
        #            if r[n1y][n1x] != '#' and visited[n1y][n1x] == math.inf:
        #                return True
    return False

#solve_race for part1
#calc cheats pos at the same time
def solve_race(r, minc=2, maxc=20):
   visited=[[math.inf for i in range(xlen)] for j in range(ylen)]
   visited[S[1]][S[0]]=0
   cheats=[]
   nc=[S]
   while len(nc)>0:
       new_nc=[]
       for p in nc:
           x,y=p
           s = visited[p[1]][p[0]]
           for di, d in enumerate(DIRS):
               nx=x+d[0]
               ny=y+d[1]
               ns=s+1
               if r[ny][nx] != '#':
                   if visited[ny][nx] > ns:
                       visited[ny][nx]=ns
                       if [nx,ny] != E: #do not continue when E is reached
                           c = r[ny][nx] 
                           #if c !='1' and c != '2':
                           r[ny][nx]='o'
                           #draw(r)
                           #input()
                           new_nc.append([nx,ny])
            
           #calculate all candidates around
           for i in range(minc, maxc+1):
                for nx in range(-i, i+1):
                    for ny in range(-i, i+1):
                        dist=abs(nx)+abs(ny)
                        if dist==i:
                            nx2=x+nx #calc point for potential cheat
                            ny2=y+ny
                 
                            cheat=[[x,y],[nx2,ny2], dist]
                            if validate_cheat(cheat, cheats, visited, r, d, di):
                                cheats.append(cheat)

       nc=new_nc
   return visited[E[1]][E[0]],cheats,visited

#copy orig race
nr=[[c for c in l] for l in race]
#resolve without the cheat
#keep visited to quickly calc wins
minc=2
maxc=20

t1, cheats,visited=solve_race(nr, 2, 20) #index 0 init time without cheating
print(f"Race finished in {t1} picos")
res={}
#calc all vert cheat (not covering the track as it is useless)

saves={}

res1=0
print(cheats)
for c in cheats: #c[0] start, c[1] end, c[2] distance
    save=visited[c[1][1]][c[1][0]]-(visited[c[0][1]][c[0][0]]+c[2])
    print(f"from {c[0]}:{visited[c[0][1]][c[0][0]]} to {c[1]}:{visited[c[1][1]][c[1][0]]}: saved {save}")
    if save >= 100:
        if save in res:
            res[save]+=1
        else:
            res[save]=1

    if save>= 100:
        res1+=1

for t in sorted(res):
    print(f"{res[t]} cheats saves {t} picos")

print(f"[SOLVED] - First star: {res1}")

#part 2
res=0
    
print(f"[SOLVED] - Second star: {res}")

#print(f"{saves}")
