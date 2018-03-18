import random

def costfunction(noofVM, noofPop):
    pop = []
    popwise = []
    random.seed(50)

    # creating random virtual machines if noofVM=5 and noofPop=3 then [[3, 4, 0, 1, 2], [3, 2, 1, 4, 0]]
    for i in range(0, noofPop):
        temp = random.sample(range(0, noofVM), noofVM)
        pop.append(temp)
    print(pop)

    # assigning types to individual vms
    aws = [[1, 1], [1, 2], [2, 4], [2, 8], [4, 16], [8, 32], [16, 64], [40, 160], [48, 192], [64, 256], [96, 384]]
    x = [random.randint(0, 10) for x in range(0, noofVM)]
    print(x)

    #assign resources to vmid
    # assigning resources to individual virtual machines based on its type
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
    print(popwise)

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
    # objective function calculation
    # if you want to implement new objective function change this code
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
    print(popwise)
    print(wastage)
    print(min(wastage))
    return popwise, wastage

# def findDistance(was,n):
#     dm=[]
#     for i in range(0, n):
#         temp = []
#         for j in range(0,n):
#            temp1=abs(was[i][0]-was[j][0])
#            temp.append(temp1)
#         dm.append(temp)
#     print(dm)



#cost function parameters
VM = 5
npop = 50
popwise,wastage=costfunction(VM, npop)

# Algorithmic Parameters
MaxIt=1000
gamma=1
beta0=2
alpha=0.2
alpha_damp=0.98
# delta=0.05*(VarMax-VarMin);     % Uniform Mutation Range
# m=2







