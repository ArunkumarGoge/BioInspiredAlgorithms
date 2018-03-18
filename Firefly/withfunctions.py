import random
import math
import operator

def createInitialPopulation(noofVM, noofPop):
    pop=[]
    random.seed(50)
    for i in range(0, noofPop):
        temp = random.sample(range(0, noofVM), noofVM)
        pop.append(temp)
    return(pop)

def createRandomResources(noofVM):
    x = [random.randint(0, 10) for x in range(0, noofVM)]
    return(x)

def AssignResources(pop,x,noofVM,noofPop):
    popwise=[]
    aws = [[1, 1], [1, 2], [2, 4], [2, 8], [4, 16], [8, 32], [16, 64], [40, 160], [48, 192], [64, 256], [96, 384]]
    for i in range(0, noofPop):
        entire = []
        for j in range(0, noofVM):
            vm = pop[i][j]
            confid = x[vm]
            cpu = aws[confid][0]
            ram = aws[confid][1]
            conf = [vm, cpu, ram]
            entire.append(conf)
        popwise.append(entire)
    return popwise

def ObjectiveFunction(noofVM, noofPop,popwise):
    physicalused = [0] * noofPop
    for i in range(0, noofPop):
        # 32 gbram * 24slots = in dell rack server
        physicalram = 768
        physicalcore = 100
        hostedin = 1
        for j in range(0, noofVM):
            if popwise[i][j][1] <= physicalcore and popwise[i][j][2] <= physicalram:
                physicalcore = physicalcore - popwise[i][j][1]
                physicalram = physicalram - popwise[i][j][2]
                popwise[i][j].append(hostedin)
            else:
                hostedin = hostedin + 1
                physicalram = 768
                physicalcore = 100
                physicalcore = physicalcore - popwise[i][j][1]
                physicalram = physicalram - popwise[i][j][2]
                popwise[i][j].append(hostedin)
        physicalused[i]=hostedin
    # print(physicalused)
    # print(popwise)


    wastage = []
    for i in range(0, noofPop):
        utilizedcpu = 0
        utilizedmem = 0
        for j in range(0, noofVM):
                utilizedcpu = utilizedcpu + popwise[i][j][1]
                utilizedmem = utilizedmem + popwise[i][j][2]
        cpuwaste = (100 * physicalused[i])-utilizedcpu
        memwaste = (768 * physicalused[i])-utilizedmem
        temp = [cpuwaste, memwaste]
        wastage.append(temp)
    return wastage

def compareVMS(A,B,vm):
    diff = list(map(operator.sub, A, B))
    # print(A)
    # print(B)
    # print(diff)
    for z in range(0, vm):
        diff[z] = (diff[z] * diff[z])
    # print(diff)
    r=math.sqrt(sum(diff))
    r=r*0.05
    # print(r)

    for i in range(0,vm):
        beta=1
        gamma=-4
        distance=math.fabs(A[i]-B[i])
        second=beta*math.exp(gamma*(r*r))*distance
        # print(second)
        B[i]=int(B[i]+second+0.5)%vm
        # print(B[i])
    # print(B)
    return B



# def findDistance(was,n):
#     dm=[]
#     for i in range(0, n):
#         temp = []
#         for j in range(0,n):
#            temp1=abs(was[i][0]-was[j][0])
#            temp.append(temp1)
#         dm.append(temp)
#     return dm


# problem parameters
VM=10
npop=40
pop=createInitialPopulation(VM,npop)
print(pop)
randres=createRandomResources(VM)
# print(randres)
popwise=AssignResources(pop,randres,VM,npop)
# print(popwise)
wastage=ObjectiveFunction(VM, npop,popwise)
print(wastage)


for i in range(0,npop):
    for j in range(0,npop):
        if wastage[i][0]<wastage[j][0]:
            pop[j]=compareVMS(pop[i],pop[j],VM)


print(pop)

