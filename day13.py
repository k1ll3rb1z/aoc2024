#!/bin/python
import math
import re

INPUT='day13.input'
#INPUT='day13.small.input'

data = open(INPUT).readlines()
prizes=[]
for i in range((len(data)+1)//4):
    for k in range(3):
        print(data[4*i+k])

    a=[int(d[2:]) for d in data[4*i].strip().split(': ')[1].split(', ')]
    b=[int(d[2:]) for d in data[4*i+1].strip().split(': ')[1].split(', ')]
    p=[int(d[2:]) for d in data[4*i+2].strip().split(': ')[1].split(', ')]

    prizes.append((a,b,p))

print(f"PRIZES")
print(f"{prizes}")

def pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
    while b!=0:
        r=a%b
        a,b=b,r
    return a

def calculate_prize(prize, rejectooexpensive=False):
    a,b,p=prize
    
    an1=p[1]-p[0]*b[1]/b[0]
    an2=a[1]-a[0]*b[1]/b[0]
    an=an1/an2

    bn1=p[1]-p[0]*a[1]/a[0]
    bn2=b[1]-b[0]*a[1]/a[0]
    bn=bn1/bn2

    #print(f"P: a={an1}/{an2} ({an1/an2}) b={bn1}/{bn2} ({bn1/bn2})")
    
    #this part is important to guess the correct numbers 
    if abs(round(an)-an)<0.0001 and abs(round(bn)-bn)<0.0001:
        an=int(round(an))
        bn=int(round(bn))
        print(f"GOOD PRIZE P {p}: {an}xA {bn}xB")
        if rejectooexpensive:
            if an > 100 or bn > 100:
                print(f"   PRIZE too expensive ")
                return 0

        return 3*an+bn
    else:

        print(f"WRONG PRIZE P {p}: {an}xA {bn}xB")
        return 0

#part 1
res=0
for p in prizes:
    res+=calculate_prize(p)
print(f"[SOLVED] - First star: {res}")

#part 2
res=0
# prizes are far away
for p in prizes:
    p[2][0]+=10000000000000
    p[2][1]+=10000000000000
    res+=calculate_prize(p)

print(f"[SOLVED] - Second star: {res}")
