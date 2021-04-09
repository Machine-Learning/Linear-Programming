# function to convert tuple to state values
def numtotuple(num):
    h = num%5
    s = (int(num/5))%2
    a = (int((int(num/5))/2))%4
    # m = (int(int((int(num/5))/2))/4)%3
    m = (int((int((int(num/5))/2))/4))%3
    p = (int((int((int((int(num/5))/2))/4))/3))%5
    return (p,m,a,s,h)



for i in range (0,100):
    print(numtotuple(i))