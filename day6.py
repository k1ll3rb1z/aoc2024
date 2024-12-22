#!/bin/python
import math
import re
import time
from curses import wrapper
import curses
import traceback

INPUT='day6.input'
#INPUT='day6.small.input'


def newpos(pos, d):
    return [pos[0]+d[0], pos[1]+d[1]]

def getposdata(pos, maze):
    return maze[pos[1]][pos[0]]

def copymaze(maze):
    newmaze=[]
    for l in maze:
        newmaze.append(l.copy())
    return newmaze


def draw_maze(stdscr, maze):
    for y, l in enumerate(maze):
        for x, c in enumerate(l):
            try:
                stdscr.addch(y, x, c)
            except:
                pass
    stdscr.refresh()
    
## to print res out of the curses app
global res1
global res2


def main(stdscr):
    global res1
    global res2

    data = open(INPUT).readlines()
    stdscr.clear()
    stdscr.border()
    k=stdscr.getkey()
    stdscr.addstr(curses.LINES-3, 10, f"   Key pressed '{repr(k)}'")
    
    # read rules and updates
    # '#' (35)  and '^' (94)
    # '.' (46)
    # 'X' (88)
    
    maze=[]
    pos=[0,0] #current guard pos

    ymax = len(data)-1
    xmax = 0 
    #remote line break
    for y,l in enumerate(data):
        l=bytearray(l.strip().encode())
        for x, c in enumerate(l):
            if c == 94:
                xmax = len(l) - 1 
                pos=(x,y)
                
                try:
                    stdscr.addstr(curses.LINES-1, 0, f"guard detected at {pos}, maze dim {xmax}x{ymax}")
                except:
                    pass

                stdscr.refresh()
                time.sleep(0.001)

    
        maze.append(l)
    
    draw_maze(stdscr, maze)
    #stdscr.getkey()

    init_pos=pos
        
    #part 1
    res=1 #visited pos, first pos is considered visited
    visited=[pos] 
    #guard walk up, right, down, left, etc .. (always turn at 90 degrees)
    dirs = [(0,-1), (1,0), (0,1), (-1,0)]
    currentdir=0

    try:
    
        while pos[0] >= 0 and pos[0] <= xmax and pos[1] >=0 and pos[1] <= ymax:
            try:
                stdscr.addch(pos[1], pos[0], 88) # 'X' 
                #stdscr.refresh()
            except:
                pass
            #time.sleep(0.00001)
            #stdscr.getkey()

            if tuple(pos) not in visited: 
                visited.append(tuple(pos))
                res+=1
            
            npos = newpos(pos,dirs[currentdir])
            try:
                if getposdata(npos, maze) == 35:
                    try:
                        stdscr.addch(npos[1], npos[0], 35)
                    except:
                        pass

                    currentdir=(currentdir+1)%4
                    npos = newpos(pos,dirs[currentdir])
                    if getposdata(npos, maze) == 35:
                        try:
                            stdscr.addch(npos[1], npos[0], 35)
                        except:
                            pass

                        currentdir=(currentdir+1)%4
                        npos = newpos(pos,dirs[currentdir])
                        if getposdata(npos, maze) == 35:
                            try:
                                stdscr.addch(npos[1], npos[0], 35)
                            except:
                                pass

                            currentdir=(currentdir+1)%4
                            npos = newpos(pos,dirs[currentdir])
                            if getposdata(npos, maze) == 35:
                                try:
                                    stdscr.addch(npos[1], npos[0], 35)
                                except:
                                    pass

                                currentdir=(currentdir+1)%4
                                npos = newpos(pos,dirs[currentdir])
            except Exception as e:
                #outof the maze
                pass

            pos = npos
    
        
        stdscr.addstr(curses.LINES-2, 0, f"[SOLVED] - First star: {res}")
        res1=res
        stdscr.addstr(curses.LINES-3, 0, f"   {len(visited)} {len(set(visited))}")
        stdscr.refresh()
    
        #part 2 caluclate all maze that would make the guard to loop
        res=0

        mazes=[]
        free_cases=0 #count free cases in the maze
        for y, l in enumerate(maze):
            for x, c in enumerate(l):
                if maze[y][x] != 35 and maze[y][x] != 94: # already an obstacle or start pos
                    
                    new_maze=copymaze(maze)
                    new_maze[y][x] = 35 #add obstacle
                    
                    stdscr.addstr(curses.LINES-4, 0, f"   Adding a new maze obstacle at {x}x{y} - {free_cases}")
                    
                    mazes.append(new_maze)

                    #draw the new maze
                    #draw_maze(stdscr, new_maze)
                    #stdscr.getkey()
                else:
                    free_cases+=1
        
        free_cases=(xmax-1)*(ymax-1)-free_cases         
        stdscr.addstr(curses.LINES-5, 30, f"free cases are {free_cases}")
        #stdscr.getkey()
        
        #print(mazes)

        for m, maze in enumerate(mazes):
            pos = init_pos
            total_cases=0
            currentdir=0
            
            draw_maze(stdscr, new_maze)
            #stdscr.getkey()
            
            while pos[0] >= 0 and pos[0] <= xmax and pos[1] >=0 and pos[1] <= ymax:
                if total_cases == free_cases:
                    stdscr.addstr(curses.LINES-1, 30,f"Loop in maze {m}")
                    res+=1 #the guard is still looping !
                    break

                try:
                    stdscr.addch(pos[1], pos[0], 88)
                except:
                    pass
                stdscr.refresh()
                time.sleep(0.01)
                
                total_cases+=1
                npos = newpos(pos,dirs[currentdir])
                try:
                    if getposdata(npos, maze) == 35:
                        currentdir=(currentdir+1)%4
                        npos = newpos(pos,dirs[currentdir])
                        if getposdata(npos, maze) == 35:
                            currentdir=(currentdir+1)%4
                            npos = newpos(pos,dirs[currentdir])
                            if getposdata(npos, maze) == 35:
                                currentdir=(currentdir+1)%4
                                npos = newpos(pos,dirs[currentdir])
                                if getposdata(npos, maze) == 35:
                                    currentdir=(currentdir+1)%4
                                    npos = newpos(pos,dirs[currentdir])
                except Exception as e:
                    #outof the maze
                    pass

                pos = npos

            stdscr.refresh()
            time.sleep(0.001)


            
        stdscr.addstr(curses.LINES-1, 0,f"[SOLVED] - Second star: {res}")
        res2=res
        stdscr.getkey() 

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        time.sleep(5)
        stdscr.getkey() 

wrapper(main)

print(f"Results First star {res1} and second star {res2}")
