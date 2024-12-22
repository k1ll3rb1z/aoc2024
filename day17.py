#!/bin/python
import math
import re
import sys
import z3

global stop,A,B,C,IP,PRG,END_PRG,output

stop=0
INPUT='day17.input'
INPUT='day17.small.input'
output=[]
try:
    INPUT = sys.argv[1]
except:
    pass

try:
    stop = int(sys.argv[2])
except:
    pass

A=0
B=0
C=0

IP=0


global enum_combo_ops

enum_combo_ops={
    0: lambda: 0,
    1: lambda: 1,
    2: lambda: 2,
    3: lambda: 3,
    4: lambda: A,
    5: lambda: B,
    6: lambda: C,
    7: lambda: None
}

# 0
def adv(x):
    global A,B,C,IP,enum_combo_ops
    IP+=2
    tmp=1<<enum_combo_ops[x]()
    A=A//tmp

# 1
def bxl(x):
    global A,B,C,IP
    IP+=2
    B=B^x

# 2
def bst(x):
    global A,B,C,IP,enum_combo_ops
    IP+=2
    B=enum_combo_ops[x]()%8
    #print(f"bst {x}: Set B to {B}")

# 3
def jnz(x):
    global A,B,C,IP,END_PRG
    if A == 0:
        print(f"End PRG detected")
        END_PRG=True
    else:
        IP=x

# 4
def bxc(x):
    global A,B,C,IP
    IP+=2
    B=B^C

# 5
def out(x):
    global A,B,C,IP,output
    IP+=2
    tmp=enum_combo_ops[x]()%8
    sys.stdout.write(f"{tmp},")
    sys.stdout.flush()

    output.append(tmp)

# 6
def bdv(x):
    global A,B,C,IP,enum_combo_ops
    IP+=2
    tmp=1<<enum_combo_ops[x]()
    B=A//tmp

# 7
def cdv(x):
    global A,B,C,IP,enum_combo_ops
    IP+=2
    tmp=1<<enum_combo_ops[x]()
    C=A//tmp

global opcodes

opcodes={
   0: adv,
   1: bxl,
   2: bst,
   3: jnz,
   4: bxc,
   5: out,
   6: bdv,
   7: cdv
}

data = open(INPUT).readlines()

#read init registers and program
A=int(data[0].strip().split(': ')[1])
B=int(data[1].strip().split(': ')[1])
C=int(data[2].strip().split(': ')[1])

PRG=[int(i) for i in data[4].strip().split(': ')[1].split(',')]

target=63687530

try:
    target=int(sys.argv[3])
    A=target
except:
    pass

print(f"PRG: {PRG} for A:{A}")
def exec_prg(prg):
    global A,B,C,IP,opcodes,END_PRG,output
    prg_len=len(prg)
    END_PRG=False
    IP=0 #start from the begining
    output=[]
    while (IP<prg_len) and (END_PRG == False):
       op,x=prg[IP:IP+2]
       if stop:
            print(f"Run instruction @{IP}: {op,x}, R -> A:{A} B:{B} C:{C}")
       opcodes[op](x)
       if stop:
            print(f"                 After {op,x}, R -> A:{A} B:{B} C:{C}")
            input()
    return output 

#part 1
exec_prg(PRG)

res=','.join([str(i) for i in output])
print(f"[SOLVED] - First star: {res}")

#############
#part 2
#trying z3

#A=z3.BitVec('a', 64)
#B=z3.BitVec(0, 64)
#C=z3.BitVec(0, 64)
#z3.solve(exec_prg(PRG) == PRG)
def calc(i=63687530):
    a=i
    print(a)
    b=0
    c=0
    out=[]
    while a != 0:
        #print(a)
        #b=(a%8)^3
        #c=a//(1<<((a%8)^3))
        #a=a//8
        #b=((a%8)^3)^5^(a//(1<<((a%8)^3)))
        b=(a%8)^6^(a//(1<<((a%8)^3)))
        a=a//8
        out.append(b%8)
    res=','.join([str(i) for i in out])
    print(res)
    return out



calc(target)
#input()
#for a in range(1,10000000000000000000):
#    calc(i=a)
#    #input()

from z3 import *

#target
targets=[2, 4, 1, 3, 7, 5, 0, 3, 1, 5, 4, 1, 5, 5, 3, 0] 

a = BitVec('a', 64)
s = z3.Solver()
for i,t in enumerate(targets):
    s.add( (UDiv(a,8**i)%8)^6^(UDiv(UDiv(a,8**i),(1<<((UDiv(a, 8**i)%8)^3)))) % 8 == t)
s.add(UDiv(a, 8**16) == 0)

while  s.check() == sat:
    v=s.model()[a].as_long()
    print(v)
    s.add(a < v)

###########
#res=0
#A=0
#output=[]
#start_A=35184000000001
#end_A= 281475000000000
########## 100000000000
#
#inc=100000000000
#inc//=1000
#
#current_A=start_A
#possible=0
#
#tested=0
#while output != PRG and tested < 100000:
#    A=current_A
#    tested+=1
#    print(f"Run PRG with A:{A} prev out len {len(output)} vs  {len(PRG)}")
#    exec_prg(PRG)
#    #if(len(output)<len(PRG):
#    #    break
#    if output[-4:-2] == PRG[-4:-2]:
#        possible+=1
#        print(f"{possible} END PRG with A:{current_A} O:{output} vs  P:{PRG}")
#    current_A+=inc 
#    
#print(f"[SOLVED] - Second star: {current_A} {possible}")
#
