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