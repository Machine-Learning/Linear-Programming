import numpy as np
import cvxpy as cp
import sys
import os
import json

MINM = -100000000

#Hyperparameters
DELTA = 0.001
GAMMA = 0.999

#Define all pos
all_pos=[]
all_pos.append('C')
all_pos.append('N')
all_pos.append('S')
all_pos.append('E')
all_pos.append('W')

#Define all state
all_states=[]
all_states.append('D')
all_states.append('R')

max_mat = 3
max_arrow = 4
max_health = 5
STEP_COST = -20
total_states = 600

#Reward for each action
action_reward = {
    'UP': STEP_COST,
    'LEFT': STEP_COST,
    'DOWN': STEP_COST,
    'RIGHT': STEP_COST,
    'STAY': STEP_COST,
    'SHOOT': STEP_COST,
    'HIT': STEP_COST,
    'CRAFT': STEP_COST,
    'GATHER': STEP_COST,
    'NONE': STEP_COST
}

#Define rewards for all states
rewards = {}
for s in all_pos:
    rewards[s] = 0

#Dictionnary of possible actions. We have two "end" states (1,2 and 2,2)
actions = {
    'W':('STAY', 'RIGHT', 'SHOOT'), 
    'N':('STAY', 'DOWN', 'CRAFT'),
    'E':('STAY', 'LEFT', 'SHOOT', 'HIT'),
    'S':('UP', 'STAY', 'GATHER'),
    'C':('STAY', 'UP', 'DOWN', 'RIGHT', 'LEFT', 'SHOOT', 'HIT')
    }

#Dictionary for integer mapping of pos of IJ
pos_map = {
    'C' : 0,
    'N' : 1,
    'S' : 2,
    'E' : 3,
    'W' : 4
}

#Dictionary for integer mapping of states of MM
state_map = {
    'D' : 0,
    'R' : 1
}

#Dictionary for integer mapping of actions
action_map = {
    'UP': 0,
    'LEFT': 1,
    'DOWN': 2,
    'RIGHT': 3,
    'STAY': 4,
    'SHOOT': 5,
    'HIT': 6,
    'CRAFT': 7,
    'GATHER': 8,
    'NONE': 9
}

final_dict = {
    "a"         : "Empty",
    "r"         : "Empty",
    "alpha"     : "Empty",
    "x"         : "Empty",
    "policy"    : "Empty",
    "objective" : "Empty",
}

#Define an initial policy
policy={}
for s in actions.keys():
    policy[s] = np.random.choice(actions[s])
print(policy)

#Define success probabilities for states
probability = {}
for s in all_pos:
    if s == 'E' or s == 'W':
        probability[s] = 1
    else:
        probability[s] = 0.85
print(probability)
        
#Define fail action for states
fail = {}
for s in all_pos:
    if s == 'E' or s == 'W':
        fail[s] = s
    else:
        fail[s] = 'E'
print(fail)

# convert tuple to number
def tupletonum(p,m,a,s,h):
    num = p*120 + m*40 + a*10 + s*5 + h
    return num

# function to convert tuple to state values
def numtotuple(num):
    h = num%5
    s = (int(num/5))%2
    a = (int((int(num/5))/2))%4
    m = (int((int((int(num/5))/2))/4))%3
    p = (int((int((int((int(num/5))/2))/4))/3))%5
    return (p,m,a,s,h)

def prob(a,p,m,arr,s,h,p1,m1,arr1,s1,h1):
    p_MM = 0
    var = 0
    if s == 'D' and s1 == 'R':
        p_MM = 0.2
    elif s == 'D' and s1 == 'D':
        p_MM = 0.8
    elif s == 'R' and s1 == 'R':
        p_MM = 0.5
    elif s == 'R' and s1 == 'D':
        p_MM = 0.5
        var = 1
    
    if var == 1 and (p == 'C' or p == 'E'):
        if arr1!=0 or m!=m1:
            return 0
        elif (h+1)!=h1 and (h!=4 or h1!=4):
            return 0
        # (h+1)==h1 or (h==4 and h1==4)
        else:
            var = 2
    if a == 'UP':
        if m!=m1 or (var!=2 and arr!=arr1) or (var!=2 and h!=h1):
            return 0
        if p == 'S':
            if p1 == 'C':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        elif p == 'C':
            if var == 2:
                if p1 == p:
                    return p_MM
                else:
                    return 0
            if p1 == 'N':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        else:
            return 0
    elif a == 'DOWN':
        if m!=m1 or (var!=2 and arr!=arr1) or (var!=2 and h!=h1):
            return 0
        if p == 'N':
            if p1 == 'C':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        elif p == 'C':
            if var == 2:
                if p1 == p:
                    return p_MM
                else:
                    return 0
            if p1 == 'S':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        else:
            return 0
    elif a == 'LEFT':
        if m!=m1 or (var!=2 and arr!=arr1) or (var!=2 and h!=h1):
            return 0
        if p == 'E':
            if var == 2:
                if p1 == p:
                    return p_MM
                else:
                    return 0
            if (p1 == 'C'):
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        elif p == 'C':
            if var == 2:
                if p1 == p:
                    return p_MM
                else:
                    return 0
            if p1 == 'W':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        else:
            return 0
    elif a == 'RIGHT':
        if m!=m1 or (var!=2 and arr!=arr1) or (var!=2 and h!=h1):
            return 0
        if p == 'W':
            if p1 == 'C':
                return probability[p]*p_MM
            elif p1 == fail[p]:
                return (1-probability[p])*p_MM
            else:
                return 0
        elif p == 'C':
            if var == 2:
                if p1 == p:
                    return p_MM
                else:
                    return 0
            if p1 == 'E':
                return 1*p_MM
            else:
                return 0
        else:
            return 0
    elif a == 'STAY':
        if m!=m1 or (var!=2 and arr!=arr1) or (var!=2 and h!=h1):
            return 0
        if var == 2 and (p == 'C' or p == 'E'):
                if p1 == p:
                    return p_MM
                else:
                    return 0
        if p1 == p:
#             print('reached 1')
            return probability[p]*p_MM
        elif p1 == fail[p]:
#             print('reached 2')
            return (1-probability[p])*p_MM
        else:
            return 0
        
    elif a == 'SHOOT':
        if p!=p1 or m!=m1:
            return 0
        if var == 2 and (p == 'C' or p == 'E'):
            if p == 'C':
                return p_MM
            elif p == 'E':
                return p_MM
        if arr == arr1+1 and (p == 'C' or p == 'E' or p == 'W'):
            if p == 'C':
                if h == h1+1:
                    return 0.5*p_MM
                elif h == h1:
                    return 0.5*p_MM
                else:
                    return 0
            elif p == 'E':
                if h == h1+1:
                    return 0.9*p_MM
                elif h == h1:
                    return 0.1*p_MM
                else:
                    return 0
            elif p == 'W':
                if h == h1+1:
                    return 0.25*p_MM
                elif h == h1:
                    return 0.75*p_MM
                else:
                    return 0
        else:
            return 0
        
    elif a == 'HIT':
        if p!=p1 or m!=m1 or (var!=2 and arr!=arr1):
            return 0
        if var == 2 and (p == 'C' or p == 'E'):
            if p == 'C':
                return p_MM
            elif p == 'E':
                return p_MM
        if p == 'C':
            if h == h1+2 or (h == h1+1 and h1 == 0):
                return 0.1*p_MM
            elif h == h1:
                return 0.9*p_MM
            else:
                return 0
        elif p == 'E':
            if h == h1+2 or (h == h1+1 and h1 == 0):
                return 0.2*p_MM
            elif h == h1:
                return 0.8*p_MM
            else:
                return 0
        else:
            return 0
        
    elif a == 'CRAFT':
        if p!=p1 or h!=h1 or m==0:
            return 0
        if p == 'N' and m>=1 and m == m1+1:
            if arr == 0:
                if arr+1 == arr1:
                    return 0.5*p_MM
                elif arr+2 == arr1:
                    return 0.35*p_MM
                elif arr+3 == arr1:
                    return 0.15*p_MM
                else:
                    return 0
            elif arr == 1:
                if arr+1 == arr1:
                    return 0.5*p_MM
                elif arr+2 == arr1:
                    return 0.5*p_MM
                else:
                    return 0
            elif arr == 2:
                if arr+1 == arr1:
                    return p_MM
                else:
                    return 0
            elif arr == 3:
                if arr == arr1:
                    return p_MM
                else:
                    return 0
        else:
            return 0
        
    elif a == 'GATHER':
        if p!=p1 or h!=h1 or arr!=arr1:
            return 0
        if p == 'S':
            if m+1 == m1 and m<=1:
                return 0.75*p_MM
            elif m == m1 and m<=1:
                return 0.25*p_MM
            elif m == m1 and m==2:
                return p_MM
            else:
                return 0
        else:
            return 0
    
    elif a == 'NONE':
        return 0
    
print(prob('CRAFT','N',1,3,'D',2,'N',1,3,'R',1))
def numtotuple(num):
    h = num%5
    s = (int(num/5))%2
    a = (int((int(num/5))/2))%4
    m = (int((int((int(num/5))/2))/4))%3
    p = (int((int((int((int(num/5))/2))/4))/3))%5
    return (p,m,a,s,h)

# print(numtotuple(193))