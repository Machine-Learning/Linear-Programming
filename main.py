import numpy as np
import sys
import os

MINM = -1000000000

#Hyperparameters
DELTA = 0.001
GAMMA = 0.999         
NOISE = 0  

#Define all pos
all_pos=[]
all_pos.append('W')
all_pos.append('N')
all_pos.append('E')
all_pos.append('S')
all_pos.append('C')

#Define all state
all_states=[]
all_states.append('D')
all_states.append('R')

max_mat = 2
max_arrow = 3
E_left = 0
max_health = 4

#Reward for each action
action_reward = {
    'UP': -10,
    'LEFT': -10,
    'DOWN': -10,
    'RIGHT': -10,
    'STAY': -10,
    'SHOOT': -10,
    'HIT': -10,
    'CRAFT': -10,
    'GATHER': -10,
    'NONE': -10
}

#Define rewards for all states
rewards = {}
for s in all_pos:
    rewards[s] = 0

#Dictionnary of possible actions. We have two "end" states (1,2 and 2,2)
actions = {
    'W':('RIGHT', 'STAY', 'SHOOT', 'NONE'), 
    'N':('DOWN', 'STAY', 'CRAFT', 'NONE'),
    'E':('LEFT', 'STAY', 'SHOOT', 'HIT', 'NONE'),
    'S':('UP', 'STAY', 'GATHER', 'NONE'),
    'C':('UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'NONE')
    }

#Dictionary for integer mapping of pos of IJ
pos_map = {
    'W' : 0,
    'N' : 1,
    'E' : 2,
    'S' : 3,
    'C' : 4
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

#Final dictionary to be converted to json and submitted
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
def tupletonum(p,m,a,s,h):
    num = p*120 + m*40 + a*10 + s*5 + h
    return num

# function to convert tuple to state values
def numtotuple(num):
    h = num%5
    s = (int(num/5))%2
    a = (int((int(num/5))/2))%4
    m = (int(int((int(num/5))/2))/4)%3
    p = (int((int(int((int(num/5))/2))/4)/3))%5
    return (p,m,a,s,h)

def prob(a,p,m,arr,s,h,p1,m1,arr1,s1,h1):
    if a == 'UP':
        if m!=m1 or arr!=arr1 or s!=s1 or h!=h1:
            return 0
        if p == 'S':
            if p1 == 'C':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        elif p == 'C':
            if p1 == 'N':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        else:
            return 0
    elif a == 'DOWN':
        if m!=m1 or arr!=arr1 or s!=s1 or h!=h1:
            return 0
        if p == 'N':
            if p1 == 'C':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        elif p == 'C':
            if p1 == 'S':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        else:
            return 0
    elif a == 'LEFT':
        if m!=m1 or arr!=arr1 or s!=s1 or h!=h1:
            return 0
        if p == 'E':
            if p1 == 'C' or (p1 == 'W' and E_left == 1):
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        elif p == 'C':
            if p1 == 'W':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        else:
            return 0
    elif a == 'RIGHT':
        if m!=m1 or arr!=arr1 or s!=s1 or h!=h1:
            return 0
        if p == 'W':
            if p1 == 'C':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        elif p == 'C':
            if p1 == 'E':
                return probability[p]
            elif p1 == fail[p]:
                return 1-probability[p]
            else:
                return 0
        else:
            return 0
    elif a == 'STAY':
        if m!=m1 or arr!=arr1 or s!=s1 or h!=h1:
            return 0
        if p1 == p:
            return probability[p]
        elif p1 == fail[p]:
            return 1-probability[p]
        else:
            return 0
        
    elif a == 'SHOOT':
        if p!=p1 or m!=m1 or s!=s1:
            return 0
        if arr == arr1+1 and (p == 'C' or p == 'E' or p == 'W'):
            if p == 'C':
                if h == h1+1:
                    return 0.5
                elif h == h1:
                    return 0.5
                else:
                    return 0
            elif p == 'E':
                if h == h1+1:
                    return 0.9
                elif h == h1:
                    return 0.1
                else:
                    return 0
            elif p == 'W':
                if h == h1+1:
                    return 0.25
                elif h == h1:
                    return 0.75
                else:
                    return 0
        else:
            return 0
        
    elif a == 'HIT':
        if p!=p1 or m!=m1 or s!=s1 or arr!=arr1:
            return 0
        if p == 'C':
            if h == h1+2:
                return 0.1
            elif h == h1:
                return 0.9
            else:
                return 0
        elif p == 'E':
            if h == h1+2:
                return 0.2
            elif h == h1:
                return 0.8
            else:
                return 0
        else:
            return 0
        
    elif a == 'CRAFT':
        if p!=p1 or s!=s1 or h!=h1:
            return 0
        if p == 'N' and m>=1 and m == m1+1:
            if arr+1 == arr1:
                return 0.5
            elif arr+2 == arr1:
                return 0.35
            elif arr+3 == arr1:
                return 0.15
            else:
                return 0
        else:
            return 0
        
    elif a == 'GATHER':
        if p!=p1 or s!=s1 or h!=h1 or arr!=arr1:
            return 0
        if p == 'S' and m<=1:
            if m+1 == m1:
                return 0.75
            elif m == m1:
                return 0.25
            else:
                return 0
        else:
            return 0
    
    elif a == 'NONE':
        return 0
r = []
a = []
col = 0
actions_list = []
for p in all_pos:
    for m in range(0,max_mat):
        for arr in range(0,max_arrow):
            for s in all_states:
                for h in range(0,max_health):
                    num_p = pos_map[p]
                    num_s = state_map[s]
                    act = []
                    for a in actions[p]:
                        if a == 'SHOOT' and arr == 0:
                            continue
                        elif a == 'CRAFT' and (m == 0 or arr == 3):
                            continue
                        elif a == 'GATHER' and m == 2:
                            continue
                        if(not h):
                            r.append(0)
                            # if unsuccessful add -40 (doubt here i.e. how to add)
                        else: 
                            r.append(action_reward[a])
                        col+=1
                        # column since later will take transpose to change to required A matrix
                        column = []
                        act.append(a)
                        add_prob = 0
                        for p1 in all_pos:
                            for m1 in range(0,max_mat):
                                for arr1 in range(0,max_arrow):
                                    for s1 in all_states:
                                        for h1 in range(0,max_health):
                                            if(p!=p1 and m!=m1 and arr!=arr1 and s!=s1 and h!=h1):
                                                pr = round(prob(a,p,m,arr,s,h,p1,m1,arr1,s1,h1),5)
                                                add_prob += pr
                                                column.append(-pr)
                        a.append(column)
                    actions_list.append(act)

print("len r : " + str(len(r)))
print(r)