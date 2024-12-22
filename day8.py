#!/bin/python
import math
import re
import itertools

INPUT='day8.input'
#INPUT='day8.small.input'


#antenna map
data = open(INPUT).readlines()

#remote line break
for i,l in enumerate(data):
    data[i]=data[i].strip()

#for each antenna seach is another antenna would create an antinode and calculate its location
class Antinode:
    x=0
    y=0
    c='#'
    ant_0=None
    ant_1=None
    index=0
    def __init__(self, x,y,ant_0, ant_1, index=0):
        self.x=x
        self.y=y
        self.ant_0=ant_0
        self.ant_1=ant_1
        self.index=index

    def print(self):
        print(f"Antinode {self.index} at {self.x}x{self.y} {str(self.ant_0)} {str(self.ant_1)}")
    
class Antenna:
    x=0
    y=0
    c='a'
    x_max=0
    y_max=0

    def __init__(self, x,y,c,x_max, y_max):
        self.x=x
        self.y=y
        self.c=c
        self.x_max=x_max
        self.y_max=y_max

    def __str__(self):
        return f"Ant '{self.c}' at {self.x}x{self.y}"
    
    # step1
    def calc_antinode(self, antenna):
        if antenna.c != self.c: #shoud be done one same antenna type
            return None #not same type

        else:
            if self.x < antenna.x:
                x_antinode=self.x+2*(antenna.x-self.x) 
            else:
                x_antinode=self.x-2*(self.x-antenna.x)

            if self.y < antenna.y:
                y_antinode=self.y+2*(antenna.y-self.y) 
            else:
                y_antinode=self.y-2*(self.y-antenna.y)

            if x_antinode < 0 or y_antinode < 0 or x_antinode > self.x_max or y_antinode > self.y_max:
                return None
                             
            return Antinode(x_antinode, y_antinode, self, antenna)
    
    #step2
    def calc_antinodes(self, antenna):
        antinodes=[]
        if antenna.c != self.c: #shoud be done one same antenna type
            return antinodes #not same type

        else:
            dist_x = abs(antenna.x-self.x)
            dist_y = abs(antenna.y-self.y)

            for i in range(1, 2+min(x_max//dist_x, y_max//dist_y)):

                 if self.x < antenna.x:
                     x_antinode=self.x+i*dist_x
                 else:
                     x_antinode=self.x-i*dist_x

                 if self.y < antenna.y:
                     y_antinode=self.y+i*dist_y
                 else:
                     y_antinode=self.y-i*dist_y

                 if x_antinode < 0 or y_antinode < 0 or x_antinode > self.x_max or y_antinode > self.y_max:
                     pass
                 else:
                     antinodes.append(Antinode(x_antinode, y_antinode, self, antenna, i))

        return antinodes


Antennas=[]
y_max=len(data)-1
for y, l in enumerate(data):
    x_max = len(l) -1
    for x, c in enumerate(l):
        if c != '.':
            Antennas.append(Antenna(x,y,c,x_max,y_max))
            # look the in the diagonals
#part 1
Antinodes=[]
Antinodes_locations=[]
res=0

print(f"Number of antennas {len(Antennas)} in map {x_max}x{y_max}")
for c in itertools.permutations(Antennas, 2):
    a=c[0].calc_antinode(c[1])
    if a is not None:
        a.print()
        #add res if antinode location does not already exists
        a_loc = (a.x, a.y)
        if a_loc not in  Antinodes_locations:
            Antinodes_locations.append(a_loc)
            res+=1
        Antinodes.append(a)

print(f"[SOLVED] - First star: {res}")

#part 2
Antinodes=[]
Antinodes_locations=[]
res=0

for c in itertools.permutations(Antennas, 2):
    #calc all antinodes
    anti_s=c[0].calc_antinodes(c[1])
    for a in anti_s:
        a.print()
        #add res if antinode location does not already exists
        a_loc = (a.x, a.y)
        if a_loc not in  Antinodes_locations:
            Antinodes_locations.append(a_loc)
            res+=1
        Antinodes.append(a)
    
print(f"[SOLVED] - Second star: {res} {len(Antinodes)}")
