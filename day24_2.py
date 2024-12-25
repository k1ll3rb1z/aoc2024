#!/bin/python
import math
import re
import sys
import itertools
import functools
from functools import lru_cache

#INPUT='day24.input'
INPUT='day24.small.input'

try:
    INPUT=sys.argv[1]
except:
    pass

ARG2=0
try:
    ARG2=int(sys.argv[2])
except:
    pass


data = open(INPUT).readlines()
data= [l.strip() for l in data]

wires_init={}
operations_init={}
op_func={
    'XOR': lambda x,y: x^y,
    'AND': lambda x,y: x&y,
    'OR': lambda x,y: x|y
}

op_func_py={
    'XOR': '^',
    'AND': '&',
    'OR': '|'
}

all_wires=[]

readop=False
for l in data:
    if len(l) == 0:
        readop=True
        continue
    if readop:
        o,w=l.split(' -> ')
        a,o,b=o.split(' ')
        if b[0] == 'x':
            operations_init[(b,o,a,w)]=0 #not exec
        else:
            operations_init[(a,o,b,w)]=0 #not exec

        all_wires.append(a)
        all_wires.append(b)
        all_wires.append(w)
    else:
        n,v=l.split(': ')
        wires_init[n]=int(v)
        all_wires.append(n)

all_wires=list(set(all_wires))
l_all_wires=len(all_wires)

def reset_computer():
    wires={}
    operations={}
    for w in wires_init:
        wires[w]=wires_init[w]
    for o in operations_init:
        operations[o]=operations_init[o]

    return wires,operations

#run computer
def run_computer():
    wires, operations=reset_computer()
    print(f"{wires}")
    print(f"{all_wires}")
    print(f"{operations}")

    #solve operations
    current_len=len(wires)
    while l_all_wires != current_len:
        print(f"{len(wires)}/{l_all_wires}") 
        prev_len=current_len
        for op in operations:
            if operations[op] == 0: #not done
                a,o,b,r=op
                if a in wires and b in wires and r not in wires:
                    wires[r] = op_func[o](wires[a],wires[b])
                    operations[op] = 1
        
        current_len=len(wires)
        if prev_len == current_len:
            break
    
    #part 1
    for w in sorted(wires.keys()):
        print(f"{w}: {wires[w]}")
    
    x=''
    y=''
    z=''
    for w in sorted(wires.keys()):
        if w[0] == 'z':
            z=str(wires[w])+z
        elif w[0] == 'y':
            y=str(wires[w])+y
        elif w[0] == 'x':
            x=str(wires[w])+x
    
    
    x=int(x,2)
    y=int(y,2)
    z=int(z,2)
    
    print(f"[SOLVED] - Second star: z:{z} x:{x} y:{y} x+y:{x+y} z == x+y:{z == x+y}")
    return z == x+y

res=run_computer()
print(f"{res}")

#calc all z equations
equations={}

#calc x equations where all operands are x,y or z
wires, operations=reset_computer()
def calcequation(v, operations):
    for o in operations:
        a,o,b,r=o
        if r == v:
            if a[0] in ['x', 'y'] and b[0] in ['x', 'y']: 
                if a[0] == 'x':
                    return f"{a}{op_func_py[o]}{b}"
                else:
                    return f"{b}{op_func_py[o]}{a}"
            elif a[0] in ['x', 'y']:
                return f"{a}{op_func_py[o]}({calcequation(b,operations)}"
            elif b[0] in ['x', 'y']:
                return f"({calcequation(a,operations)}){op_func_py[o]}{b}"
            else:
                return f"({calcequation(a,operations)}){op_func_py[o]}({calcequation(b,operations)})"
                

def calc_equations():
    wires, operations=reset_computer()
    for i in range(46):
        v=f"z{i:02d}"
        for o in operations:
            a,o,b,r=o
            if r == v:
                equations[v]=calcequation(v,operations)
                break

calc_equations()

for e in equations:
    print(f"{e}={equations[e]}")

#calc carry
def calccarry(i, operations):
    if i==-1:
        return "0"
    else:
        x=f"x{i:02d}"
        y=f"y{i:02d}"
        
        c_prev=calccarry(i-1, operations)
        if c_prev == "0":
            for o in operations:
                a,o,b,r=o
                if x == a and y == b and o == 'AND':
                    return r
            return f"{x}&{y}"
        else:
            xor_exp=f"({x}^{y})"
            and_exp=f"({x}&{y})"
            for o in operations:
                a,o,b,r=o
                if x == a and y == b:
                    if o == 'AND':
                        and_exp=r
                    elif o == 'XOR':
                        xor_exp=r

            and2_exp=f"({xor_exp}&{c_prev})"
            for o in operations:
                a,o,b,r=o
                if o == 'AND' and ((a == xor_exp and b == c_prev) or (b == xor_exp and a == c_prev) ):
                    print(f"Replace {and2_exp} by {r}")
                    and2_exp=r 
            
            or_exp=f"({and2_exp}|{and_exp})"
            for o in operations:
                a,o,b,r=o
                if o == 'OR' and ((a == and2_exp and b == and_exp) or (a == and_exp and b == and2_exp) ):
                    or_exp=r 

            return or_exp

#calc equation at index i

def calcgoodeq(i, operations):
    print(f"Calc z{i:02d}") 
    x=f"x{i:02d}"
    y=f"y{i:02d}"
    z=f"z{i:02d}"

    if i == 0:
        xor_exp=f"({x}^{y})"
        for o in operations:
            a,o,b,r=o
            if x == a and y == b and o == 'XOR':
                c=calccarry(i-1, operations)
                xor_exp=r
                break
        return xor_exp
    else:
        c=f"{calccarry(i-1,operations)}"
        xor_exp=f"({x}^{y})"
        for o in operations:
            a,o,b,r=o
            if x == a and y == b and o == 'XOR':
                c=calccarry(i-1, operations)
                xor_exp=r
                break
        #check if op is avail
        final_exp=f"{c}^{xor_exp}"
        for o in operations:
            a,o,b,r=o
            if ((a == c and b == xor_exp) or (a == xor_exp and b == c)) and o == 'XOR':
                final_exp=r
                break

        #if z != final_exp:
        #    print(f"Change {z} and {final_exp}")
        #    input()

        return final_exp
    
changes=[]
def calc_good_equations():
    wires, operations=reset_computer()
    good_equations={}
    restart=False
    for i in range(46):
        z=f"z{i:02d}"
        g=calcgoodeq(i, operations)
        if g != z and len(changes) < 8:
             input()
             del_o1=None
             add_o1=None
             del_o2=None
             add_o1=None
             if len(g) == 3:
                 print(f"Change {z} and {g}")
                 changes.append(z)
                 changes.append(g)
                 for o in operations_init:
                      a,op,b,r=o
                      if r == g:
                          del_o1=o
                          add_o1=(a,op,b,z)
                      if r == z:
                          del_o2=o
                          add_o2=(a,op,b,g)

             else:
                 ex1=None
                 ex2=None
                 for o in operations_init:
                      a,op,b,r=o
                      x=g[:3]
                      y=g[4:]

                      if r == z:
                          if a == x:
                              print(f"{b} <-> {y}")
                              ex1=b
                              ex2=y
                          elif a == y:
                              print(f"{b} <-> {x}")
                              ex1=b
                              ex2=x
                          elif b == x:
                              print(f"{a} <-> {y}")
                              ex1=a
                              ex2=y
                          elif b == y:
                              print(f"{a} <-> {x}")
                              ex1=a
                              ex2=x
                          else:
                              print(f"Error: not exchange found")

                 changes.append(ex1)
                 changes.append(ex2)
                 for o in operations_init:
                      a,op,b,r=o
                      if r == ex1:
                          del_o1=o
                          add_o1=(a,op,b,ex2)
                      if r == ex2:
                          del_o2=o
                          add_o2=(a,op,b,ex1)

             del operations_init[del_o1]
             del operations_init[del_o2]
             operations_init[add_o1]=0
             operations_init[add_o2]=0
             restart=True
             break

        good_equations[z]=g
        print(f"{z}={g}")
        print(f"{z}={equations[z]}")
    
    if restart:
        good_equations=calc_good_equations()

    return good_equations

good_equations=calc_good_equations()
for e in good_equations:
    print(f"{e}={good_equations[e]}")
    #input()
print(",".join(sorted(changes)))
#for o in sorted(operations_init):
#    print(f"{o}")
# shj <-> z07
# tpk <-> wkb
# z23 <-> pfn
# z27 <-> kcd
 
