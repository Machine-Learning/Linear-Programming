import numpy as np
import cvxpy as cp
import logging

# Basic configuration for logging into info file
logging.basicConfig(filename="info.log",filemode='w',format='%(message)s', level=logging.INFO)
logging.info("Info File")

# position dictionary
pos_dict = {
    0:'W',
    1:'N',
    2:'E',
    3:'S',
    4:'C'
}

# MM state dictionary
mm_state_dict = {
    0:'D',
    1:'R'
}

# action dictionary
action_dict = {
    0:'UP',
    1:'LEFT',
    2:'DOWN',
    3:'RIGHT',
    4:'STAY',
    5:'SHOOT',
    6:'HIT',
    7:'CRAFT',
    8:'GATHER',
    9:'NONE'
}

# Final dictionary to be converted to json and submitted
final_dict = {
    "a"         : "Empty",
    "r"         : "Empty",
    "alpha"     : "Empty",
    "x"         : "Empty",
    "policy"    : "Empty",
    "objective" : "Empty",
}

# state (position,material,arrow,state,health)
# position = {W=0, N=1, E=2, S=3, C=4}
# material = {0, 1, 2}
# arrow    = {0, 1, 2, 3}
# MM state = {D=0, R=1}
# health   = {0,1,2,3,4} x 25

# reward should be updated tomorrow
reward = 0

# set all states { total states count 600 = 5*3*4*2*5}
states = []
for i in range(0,5):
    for j in range(0,3):
        for k in range(0,4):
            for l in range(0,2):
                for m in range(0,5):
                    states.append([(i,j,k,l,m),reward])

# probabilities 

# to be defined