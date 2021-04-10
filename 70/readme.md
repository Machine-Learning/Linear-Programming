# MDL Assignment 2 Part 3

## Team Name: Genetic Algo
## Team Number: 70

## Team Members :
    - Utkarsh Upadhyay ( 2019101010 )
    - Prince Singh Tomar ( 2019101021 )

### Initial State : (CENTER,2,3,R,4)
### Step Cost : -10

## Procedure of making A matrix : 

For Finding A matrix, We looped over all the possible initial states. If in the state Mighty Monsters has health 0 then Indiana Jones Work is done hence they are End states, hence we made column list as 0 at all other instance except for the given state where it is 1. If in the state Mighty Monster's health is not zero then we are looping over all the actions for that state and for the actions we are finding next state, after finding the next state we append the probability of that transition in the column list. If the Final and Initial State are same then we are appending Zero. Later after appending all the probability values of all possible next states, We know that sum of all the values in A matrix for an action is zero, hence we are adding all the appended probability values and setting it's negation to that of current initial state . Later we are taking transpose to make it correct.



## Procedure of finding Policy :

In our alpha vector, we have taken (C,2,3,R,4) as the only possible initial state.
For R vector, we added STEP_COST for every action (except for NONE action), and then if MM is successfully attacking IJ in the initial pos, 
additional cost of -40 was added.
Correct Values of X are calculated using linear programming
Constraints :
    AX = alpha
    X >= 0

Now since Every possible state has set of Values corresponding to their actions. Among these we stated with possible action as 1st action 
and comparing its values with other values of actions in the same state and thereby finding and updating final action as the one with 
highest value.



## Anayzing the Result :
- Center :
>   If Indiana Jones has arrows but less material and the Mighty Monster is in Dormat state then Indiana Jones SHOOTS.
>   If Indiana Jones had no arrows and material then Indiana jones will move to RIGHT.  
>   If Indiana Jones had material but no arrows then Indiana Jones move UP.
>   If Indiana Jones had arrows and Mighty Monster had very less health then Indiana Jones shoots.

- South :
>   If Indiana Jones had no materials and Mighty Monster is in Active State then Indiana Jones GATHERS.
>   If Indiana Jones had arrows and Mighty Monster in Dormat State then Indiana Jones moves UP.
>   If Mighty Monster is in active state then Indiana Jones STAYS.

- North:
>   If MM is in Ready state, IJ prefers to stay in this pos by CRAFT or STAY action.
>   If MM is in Dormant state, IJ usually moves down to attack the MM.

- East:
>   Here IJ may either HIT or SHOOT MM. HIT action is preferred if MM has high health, else SHOOT action is preferred.

- West:
>   If MM has low health, IJ prefers to SHOOT from here.
>   If MM has higher health and is in READY state, IJ prefers to STAY.
>   If MM has higher health and is in DORMANT state, then IJ moves RIGHT.

## Can there be multiple policies?
Yes we can obtain different policies by making the following changes:
* If the alpha vector is changed we would get a different policy. We could change the intial start state to some other state or even have multiple start states represented in the alpha vector as a probability distribution. (This change wouldn't affect A matrix and the R vector)
* Another change can be made in the policy by changing how we select the best action if multiple actions have the same value. Currently we have the picked the last action with highest value, but instead, for ex, if we picked the first action with highest value, we would get a different policy. (However, this change would not have any effect on A matrix, R vector, Alpha vector)