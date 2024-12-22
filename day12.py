#!/bin/python
import math
import re
import sys

INPUT='day12.input'
#INPUT='day12.small3.input'
#INPUT='day12.small2.input'
INPUT='day12.small4.input'
#INPUT='day12.small5.input'
#INPUT='day12.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

global garden, visited,y_max,x_max,dirs, empty_visited

garden = open(INPUT).readlines()
y_max=len(garden)-1
x_max=0
     #left, up, right, down
dirs=[(-1,0),(0,-1),(1,0),(0,1)]

visited=[]
#prepare garden
for y, l in enumerate(garden):
    l=l.strip()
    garden[y]=l
    if not x_max:
        x_max = len(l)-1
    visited.append((x_max+1)*[0])


def getempty():
    global x_max, y_max
    empty=[]
    for x in range(y_max+1):
        empty.append([0] * (x_max+1))
    return empty

empty_visited=getempty()

print(f"Working on a {x_max+1}x{y_max+1} garden")
print(f"{garden}")

global around_perim
around_perim={
    1:2, 
    2:0, 
    3:-2, 
    4:-4
}

square_count_enum1={
    0: 0,
    1: 2,
    2: 4
}

##
#x -4
##

###
#X
##

###
#X
###

square_count_enum3={
    0: -4,
    1: -2,
    2: 0
}
square_count_enum2_1={
    0: -4,
    1: -2,
    2: 0,
    3: 2,
    4: 4
}

square_count_enum2_2={
    0: -2,
    1: 0,
    2: 2
}

#from x,y to n_x,n_y with dir d
def calculate_sides_update(x, y, n_x, n_y, c, d_i):
    global garden, visited,x_max,y_max,dirs, around_perim
 
    print(f"{c} sides update {x,y} to {n_x, n_y} D:{d_i}")
    count=0
    ret=0
    d1=dirs[(d_i+1)%4]
    d2=dirs[(d_i-1)%4]
    
    # c c
    # X X c
    # c c

    n1_x = x+d1[0]
    n1_y = y+d1[1]

    n2_x = x+d2[0]
    n2_y = y+d2[1]
    
    #list of empty around with the used dir index
    d_empty_list=[]
    #na_x, na_y is point around n_x,n_y
    for d_i, d in enumerate(dirs):
        na_x = n_x+d[0]
        na_y = n_y+d[1]
        if na_x>=0 and na_x<=x_max and na_y>=0 and na_y<=y_max:
            if visited[na_y][na_x] == 1:
                nc = garden[na_y][na_x]
                if nc == c:#same type
                    count+=1
                else:
                    d_empty_list.append(d_i)

            else:#empty
                print(f"{c} from {x}x{y} adding dir {d_i} to empty list {d_empty_list}")
                d_empty_list.append(d_i)
        else:#outside is considered empty
            print(f"{c} from {x}x{y} adding outside dir {d_i} to empty list {d_empty_list}")
            d_empty_list.append(d_i)


    #count is the number of point already visited with the same type 
    if count == 4:
        print(f"{c} No empty at {n_x, n_y} Surrounded D:{d_empty_list}")
        ret=-4

    if count == 3:
        #d_empty_list should have only one dir (the from point)
        print(f"{c} Single empty at {n_x, n_y} D:{d_empty_list}")
        #3 cases
        # ##  # # #
        # #x  #x# #X#
        # ##  ### ###
        i_d=d_empty_list[0]

        d1=dirs[(i_d+1)%4]
        d2=dirs[(i_d-1)%4]

        #pos of the empty square
        ne_x=n_x+dirs[i_d][0]
        ne_y=n_y+dirs[i_d][1]

        #check from the empty square in d1 and d2 dirs
        ne1_x=ne_x+d1[0]
        ne1_y=ne_y+d1[1]

        ne2_x=ne_x+d2[0]
        ne2_y=ne_y+d2[1]

        square_count=0
        if ne1_x>=0 and ne1_x<=x_max and ne1_y>=0 and ne1_y<=y_max:
            n1_c = garden[ne1_y][ne1_x]
            if visited[ne1_y][ne1_x] == 1 and n1_c == c:
                square_count+=1
        if ne2_x>=0 and ne2_x<=x_max and ne2_y>=0 and ne2_y<=y_max:
            n2_c = garden[ne2_y][ne2_x]
            if visited[ne2_y][ne2_x] == 1 and n2_c == c:
                square_count+=1
        ret=square_count_enum3[square_count]

    if count == 2:
        print(f"{c} Two empty at {n_x, n_y} D:{d_empty_list}")
        #several cases
        #       #       #      #X       #X      #X X    #X X
        #XX -2  #XoX -4 #XXX 0 #XoXX -1 #XoXX 0 #XoXx 2 #XoX 4
        #Xo     #       #Xo    #        #X      #X      #X X
        #

        #XXX
        #Xo  2
        #X

        id1, id2 = d_empty_list


        #left and right from empty 1 and 2
        d1_1=dirs[(id1+1)%4]
        d2_1=dirs[(id1-1)%4]
        
        d1_2=dirs[(id2+1)%4]
        d2_2=dirs[(id2-1)%4]

        #pos of the empty square
        ne1_x=n_x+dirs[id1][0]
        ne1_y=n_y+dirs[id1][1]

        ne2_x=n_x+dirs[id2][0]
        ne2_y=n_y+dirs[id2][1]

        #check from the empty square in d1 and d2 dirs
        ne11_x=ne1_x+d1_1[0]
        ne11_y=ne1_y+d1_1[1]

        ne12_x=ne1_x+d2_1[0]
        ne12_y=ne1_y+d2_1[1]

        ne21_x=ne2_x+d1_2[0]
        ne21_y=ne2_y+d1_2[1]

        ne22_x=ne2_x+d2_2[0]
        ne22_y=ne2_y+d2_2[1]

        # remove both points which are the same
        points=[(ne11_x, ne11_y),(ne12_x, ne12_y),(ne21_x,ne21_y), (ne22_x,ne22_y)]


        dist = abs(id1-id2)
        if dist == 2: #opposit dir
            #5 cases
            square_count=0
            for p in points:
               if p[0] >= 0 and p[0] <=x_max and p[1] >=0 and p[1] <=y_max:
                   n_c = garden[p[1]][p[0]]
                   if visited[p[1]][p[0]] == 1 and n_c == c:
                       square_count+=1
            
            ret=square_count_enum2_1[square_count]
        else:
            #3 cases
            
            #left and right from empty 1 and 2
            # remove both points which are the same
            points=[(ne11_x, ne11_y),(ne12_x, ne12_y),(ne21_x,ne21_y), (ne22_x,ne22_y)]
            points_set={}
            for p in points:
                if p in points_set:
                    points_set[p]+=1 #should be removed
                    print(f"Sort points: remove {p}")
                else:
                    points_set[p]=1
            
            points=[]
            for p in points_set:
                if  points_set[p]==1:
                    points.append(p)
            
            square_count=0
            for p in points:
               if p[0] >= 0 and p[0] <=x_max and p[1] >=0 and p[1] <=y_max:
                   n_c = garden[p[1]][p[0]]
                   if visited[p[1]][p[0]] == 1 and n_c == c:
                       square_count+=1
            
            ret=square_count_enum2_2[square_count]

    if count == 1:
        print(f"{c} Three empty at {n_x, n_y} D:{d_empty_list}")
        #3 cases
        #X
        #Xx
        #X
        square_count=0
        if n1_x>=0 and n1_x<=x_max and n1_y>=0 and n1_y<=y_max:
            n1_c = garden[n1_y][n1_x]
            if visited[n1_y][n1_x] == 1 and n1_c == c:
                square_count+=1 
        if n2_x>=0 and n2_x<=x_max and n2_y>=0 and n2_y<=y_max:
            n2_c = garden[n2_y][n2_x]
            if visited[n2_y][n2_x] == 1 and n2_c == c:
                square_count+=1
        ret=square_count_enum1[square_count]
    

    print(f"{c} from {x,y} to {n_x, n_y} updates sides with {ret}")
    return ret

#part2
# get all loc from on point with same type and long sides
def getareasametype_longside(x,y, c, c_surf=1, c_sides=4):
    global garden, visited,x_max,y_max,dirs
    locs=[]
    visited[y][x]=1
    #print(f"{c} mark {x}*{y} as visited")
    #currebt surf and perimeter
    surf=c_surf
    sides=c_sides
    print(f"{c} from {x,y} S:{sides}")
    for d_i, d in enumerate(dirs):
        n_x = x+d[0]
        n_y = y+d[1]
        #print(f"look at new loc {n_x}x{n_y}")
        if n_x>=0 and n_x<=x_max and n_y>=0 and n_y<=y_max:
            if visited[n_y][n_x] == 0:
                nc = garden[n_y][n_x]
                if nc == c:#same type
                    locs.append((n_x, n_y))
                    #print(f"{c} mark {n_x}*{n_y} as visited")
                    visited[n_y][n_x] = 1
                    surf+=1
                    # lets count sides modification
                    sides+=calculate_sides_update(x, y, n_x, n_y, c, d_i)

                    print(f"{c} from {x,y} update sides S:{sides}")
    for l in locs:
        surf, sides = getareasametype_longside(l[0], l[1], c, surf, sides)
    
    return surf, sides

def getsametypevisitedaround(x,y,c):
    global garden, visited,x_max,y_max,dirs, around_perim
 
    count=0
    for d in dirs:
        n_x = x+d[0]
        n_y = y+d[1]
        if n_x>=0 and n_x<=x_max and n_y>=0 and n_y<=y_max:
            if visited[n_y][n_x] == 1:
                nc = garden[n_y][n_x]
                if nc == c:#same type
                    count+=1
    return around_perim[count]


#part1
# get all loc from on point with same type
def getareasametype(x, y, c, c_surf=1, c_perim=4):
    global garden, visited,x_max,y_max,dirs
    locs=[]
    visited[y][x]=1
    #currebt surf and perimeter
    surf=c_surf
    perim=c_perim

    for d_i, d in enumerate(dirs):
        n_x = x+d[0]
        n_y = y+d[1]
        #print(f"look at new loc {n_x}x{n_y}")
        if n_x>=0 and n_x<=x_max and n_y>=0 and n_y<=y_max:
            if visited[n_y][n_x] == 0:
                nc = garden[n_y][n_x]
                if nc == c:#same type
                    locs.append((n_x, n_y))
                    visited[n_y][n_x] = 1
                    surf+=1
                    perim+=getsametypevisitedaround(n_x, n_y, c)
                    #adjust perim depending on how many visited around with same type
    for l in locs:
        surf, perim = getareasametype(l[0], l[1], c, surf, perim)
    
    return surf, perim

def visite_new_area(x,y):
    global garden, visited
    p=garden[y][x]
    while True:
        for d in dirs:
            pass

#part 1
res=0
for y, l in enumerate(garden):
    for x, c in enumerate(l):
        if visited[y][x] == 0:#new garden
            surf, perim = getareasametype(x,y,c)
            print(f"New area {c} covered from {x}x{y} S:{surf} P:{perim}")
            res+=surf*perim

print(f"[SOLVED] - First star: {res}")

#part 2
print("PART 2")
res=0
visited=getempty()
#print(f"{visited}")

for y, l in enumerate(garden):
    for x, c in enumerate(l):
        if visited[y][x] == 0:#new garden
            area=getempty()
            print(f"Calculating area {c} from {x}x{y}")
            surf, sides = getareasametype_longside(x,y,c)
            print(f"New area {c} covered from {x}x{y} S:{surf} L:{sides}")
            res+=surf*sides
    
print(f"[SOLVED] - Second star: {res}")
