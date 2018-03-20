import random
import math
import operator


#This function will create the initial population without repetitions
#If noofVM=5 and noofPop=2 then the pop will be [[3, 2, 1, 0, 4], [2, 0, 4, 1, 3]]
#seed is used to create same set of random variable in each execution
def createInitialPopulation(noofVM, noofPop):
    pop=[]
    random.seed(50)
    for i in range(0, noofPop):
        temp = random.sample(range(0, noofVM), noofVM)
        pop.append(temp)
    return(pop)

#This function will create set of values with repetitions [10, 8, 1, 2, 5] in range 0 t0 10
#These values decides the resources to be assigned to for individual virtual machine
def createRandomResources(noofVM):
    x = [random.randint(0, 10) for x in range(0, noofVM)]
    return(x)

#Here we are passing the initially created value from createInitialPopulation() and createRandomResources()
#pop has [[3, 2, 1, 0, 4], [2, 0, 4, 1, 3]]
#x has [10, 8, 1, 2, 5]
#For the above example the VM with id 3 is of aws type 1 and this function will assign the resource
#For the above example the VM with id 0 is of aws type 10
#[[3, 2, 4], [2, 1, 2], [1, 48, 192], [0, 96, 384], [4, 8, 32]] [vmid,cpu,ram]
#The types of virtual machines are extracted from https://aws.amazon.com/ec2/
def AssignResources(pop,x):
    noofVM=len(pop[1])
    noofPop=len(pop)
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


#Wastage for individual population is calculated considering there are infinite pyhsical machine
def ObjectiveFunction(popwise):
    noofVM=len(popwise[1])
    noofPop=len(popwise)
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


#Actual firefly algorithm implementation based on the manuscript
#Yang, Xin-She. "Firefly algorithms for multimodal optimization."
# International symposium on stochastic algorithms. Springer, Berlin, Heidelberg, 2009.
def firefly(A,B):
    vm=len(A)
    diff = list(map(operator.sub, A, B))
    for z in range(0, vm):
        diff[z] = (diff[z] * diff[z])
    r=math.sqrt(sum(diff))
    r=r*0.05
    for i in range(0,vm):
        beta=1
        gamma=-4
        distance=math.fabs(A[i]-B[i])
        second=beta*math.exp(gamma*(r*r))*distance
        B[i]=int(B[i]+second+0.5)%vm
    B=SolutionRepair(B)
    return B


#When applying the algorithm the population may end up with repeated values like [4,4,0,1,3]
#We are using this function to eliminate the repetiton and insert the missing VMid in the repeated place
def SolutionRepair(x):
    size=len(x)
    temp = random.sample(range(0, size), size)
    temp.sort()
    z = list(set(temp) - set(x))
    z.sort()
    flag = [0] * size
    for i in range(0, len(x)):
        dre = x[i]
        if flag[dre] == 0:
            flag[dre] = 1
        else:
            min = 10000
            for j in range(0, len(z)):
                if (int(math.fabs(z[j] - dre) < min)):
                    min = math.fabs(z[j] - dre)
                    index = j
            dre2 = z[index]
            flag[dre2] = 1
            x[i] = z[index]
            z.remove(z[index])
    return(x)



# problem parameters
VM=5
npop=2
pop=createInitialPopulation(VM,npop)
print(pop)
randres=createRandomResources(VM)
print(randres)
popwise=AssignResources(pop,randres)
print(popwise)
wastage=ObjectiveFunction(popwise)
print(wastage)


for i in range(0,npop):
    for j in range(0,npop):
        if wastage[i][0]<wastage[j][0]:
            pop[j]=firefly(pop[i],pop[j])


print(pop)

