import random
import math

def candidateSolGen(noofVM, noofPop):
    pop = []
    popwise = []
    random.seed(0)

    for i in range(0, noofPop):
        temp = random.sample(range(0, noofVM), noofVM)
        pop.append(temp)
    print(pop)

    # assigning types to individual vms
    aws = [[1, 1], [1, 2], [2, 4], [2, 8], [4, 16], [8, 32], [16, 64], [40, 160], [48, 192], [64, 256], [96, 384]]
    x = [random.randint(0, 10) for x in range(0, noofVM)]
    # print(x)

    # assigning resources to individual
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
    # print(popwise)

    for i in range(0, noofPop):
        # 16 gbram * 24slots = in dell rack server
        physicalram = 756
        physicalcore = 100
        hostedin = 1
        for j in range(0, noofVM):
            if popwise[i][j][1] <= physicalcore and popwise[i][j][2] <= physicalram:
                physicalcore = physicalcore - popwise[i][j][1]
                physicalram = physicalram - popwise[i][j][2]
                popwise[i][j].append(hostedin)
            else:
                hostedin = hostedin + 1
                physicalram = 756
                physicalcore = 100
                physicalcore = physicalcore - popwise[i][j][1]
                physicalram = physicalram - popwise[i][j][2]
                popwise[i][j].append(hostedin)
    print(popwise)

    # waste calaculation per population [cpuwastage,memwastage]
    wastage = []
    for i in range(0, noofPop):
        utilizedcpu = 0
        utilizedmem = 0
        vmid = 1
        for j in range(0, noofVM):
            if popwise[i][j][3] == vmid:
                utilizedcpu = utilizedcpu + popwise[i][j][1]
                utilizedmem = utilizedmem + popwise[i][j][2]
            else:
                vmid = vmid + 1
                utilizedcpu = utilizedcpu + popwise[i][j][1]
                utilizedmem = utilizedmem + popwise[i][j][2]
        cpuwaste = (100 * vmid) - utilizedcpu
        memwaste = (756 * vmid) - utilizedmem
        temp = [cpuwaste, memwaste]
        wastage.append(temp)
    print(wastage)
    # print(max(wastage))
    return popwise,wastage

def findDistance(was,n):
    dm=[]
    for i in range(0, n):
        temp = []
        for j in range(0,n):
           temp1=abs(was[i][0]-was[j][0])
           temp.append(temp1)
        dm.append(temp)
    print(dm)




VM = 5
pop = 50
popwise,wastage=candidateSolGen(VM, pop)
gb=min(wastage)
distance = findDistance(wastage,pop)
maxiteration=100