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
STEP_COST = -10
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

r = []
A = []
temp_x = []
policy = []
col = 0
flag = 0

# prev_state = np.zeros((len(all_pos),max_mat,max_arrow,len(all_states),max_health), dtype=object)
# prev_state = [[[[[[] for i in range(max_health)] for i in range(len(all_states))] for i in range(max_arrow)] for i in range(max_mat)] for i in range(len(all_pos))]

for p in all_pos:
    for m in range(0,max_mat):
        for arr in range(0,max_arrow):
            for s in all_states:
                for h in range(0,max_health):
                    num_p = pos_map[p]
                    num_s = state_map[s]
                    column = []
                    tmp = []
                    # column = [] ---> 
                    if( h == 0 ):
                        for i in range(0,total_states):
                            (p1,m1,arr1,s1,h1) = numtotuple(i)
                            if(pos_map[p]!=p1 or m!=m1 or arr!=arr1 or state_map[s]!=s1 or h!=h1):
                                column.append(0)
                            else:
                                column.append(1)
                        tmp.append(0)
                        r.append(tmp)
                        col+=1
                        # print(column)
                        A.append(column)
                        continue
                    # print('Initial state: ',p,m,arr,s,h)
                    for a in actions[p]:
                        if a == 'SHOOT' and arr == 0:
                            continue
                        elif a == 'CRAFT' and (m == 0):
                            continue
                        # if unsuccessful add -40 (doubt here i.e. how to add)
                        tmp.append(STEP_COST)
                        col+=1
                        column = []
                        # print('\tAction: ',a)
                        # column since later will take transpose to change to required A matrix
                        for p1 in all_pos:
                            for m1 in range(0,max_mat):
                                for arr1 in range(0,max_arrow):
                                    for s1 in all_states:
                                        for h1 in range(0,max_health):
                                            if(p!=p1 or m!=m1 or arr!=arr1 or s!=s1 or h!=h1):
                                                pr = prob(a,p,m,arr,s,h,p1,m1,arr1,s1,h1)
                                                # print('\t\tFinal state: ',p1,m1,arr1,s1,h1,';\tProb: ',pr)
                                                column.append(-pr)
                                                if s == 'R' and s1 == 'D' and (p == 'E' or p == 'C') and ((h+1)==h1 or (h==4 and h1==4)) and arr1==0 and m==m1:
                                                    tmp[-1] -= 40*pr
                                                # if(pr != 0):
                                                #     print(pr)
                                            else:
                                                column.append(0)
                        type_col = sum(column)
                        # print(type_col)
                        column[tupletonum(pos_map[p],m,arr,state_map[s],h)] = -type_col
                        # print(column)
                        A.append(column)
                    r.append(tmp)
                    # if(flag == 0):
                    #     flag= 1
                    #     for i in column:
                    #         print(i)
                # for i in range(len(A)):
                #     for j in range(len(A[i])):
                #         print(A[i][j],end=' ')
                #     print()
                # print('---------------------------------------------------------')
                # exit()
# print(A)
# print(r)
# r_prev = r
# for p in all_pos:
#     for m in range(0,max_mat):
#         for arr in range(0,max_arrow):
#             for s in all_states:
#                 for h in range(0,max_health):
#                     num_p = pos_map[p]
#                     num_s = state_map[s]
#                     val = tupletonum(pos_map[p],m,arr,state_map[s],h)
#                     # print(val)
#                     rew = r[val][0]
#                     # print('Len = ',len(prev_state[num_p][m][arr][num_s][h]))
#                     for i in range(len(prev_state[num_p][m][arr][num_s][h])):
#                         j = prev_state[num_p][m][arr][num_s][h][i]
#                         # print('PREV state: ',j,end='; ')
#                         # print('\t',i)
#                         # print('Final state: ',p,m,arr,s,h)
#                         if j[3] == 'R' and s == 'D' and (j[0] == 'E' or j[0] == 'C') and ((j[4]+1)==h or (j[4]==4 and h==4)) and arr==0 and j[1]==m:
#                             # print('Initial',r[val][i],end=' ')
#                             rew -= 40*0.5
#                             # print('Final', r[val][i])
#                         # if s == 'R' and s1 == 'D' and (p == 'E' or p == 'C') and ((h+1)==h1 or (h==4 and h1==4)) and arr1==0 and m==m1:
#                     for i in range(len(r[val])):
#                         r[val][i] = rew


# Opening JSON file
with open('part_3_output.json') as json_file:
    data = json.load(json_file)
# cnt = 0
# j = 0
# for i in range(len(r)):
#     for j in range(len(r[i])):
#         print('i=',cnt,'; Our: ',r[i][j],', Their: ',data['r'][cnt])
#         if data['r'][cnt] != r[i][j]:
#             print(numtotuple(i))
#         cnt += 1
        
r_final = []
for i in range(len(r)):
    for j in range(len(r[i])):
        r_final.append(r[i][j])
r = np.array(r_final)
r.shape = (1,-1)

# for i in r.tolist():
#     print(i)
  
    # Print the type of data variable
    # print("Type:", type(data))
  
    # Print the data of dictionary
    # print("\nR:", data['r'])
    # print("\nPeople2:", data['people2'])

        # break

A = np.array(A)
# transpose of A
data['a'] = np.array(data['a'])
data['a'] = np.transpose(data['a'])
print("A : ")
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        print('i=',i,',j=',j,', OUR: ',A[i][j],'Their: ',data['a'][i][j])
        if abs(A[i][j] - data['a'][i][j]) > 1e-8:
            print("DIFF, INI: ",numtotuple(i))
    print()
A = np.transpose(A)

alpha = [0 for i in range(0,total_states)]
alpha[tupletonum(pos_map['W'],0,0,state_map['D'],0)] = 1
alpha = np.array(alpha)
alpha.shape = (total_states,1)

# final_dict = {
    # "a"         : "Empty",
    # "r"         : "Empty",
    # "alpha"     : "Empty",
    # "x"         : "Empty",
    # "policy"    : "Empty",
    # "objective" : "Empty",
# }

# update some values in final dictionary
final_dict['a'] = A.tolist()
final_dict['r'] = r_final
final_dict['alpha'] = alpha.tolist()

# Linear Programming
x = cp.Variable(shape=(col,1), name="x")

print("r : " + str(r.shape))
print("A : " + str(A.shape))
print("x : " + str(x.shape))
print("alpha : " + str(alpha.shape))

constraints = [cp.matmul(A, x) == alpha, x>=0]
objective = cp.Maximize(cp.matmul(r,x))
problem = cp.Problem(objective, constraints)
solution = problem.solve()

print(problem.status)
print(problem.value)

# for getting values of x

for i in x.value:
    temp_x.append(i[0])

final_dict['objective'] = solution
final_dict['x'] = temp_x

# index,st = 0,0

# for a in all_pos:
