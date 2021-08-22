def getFittestIndex(sorted_list): #falling roof method
    prob_list = getProbList(sorted_list)
    resultIndex = -1
    upperDouble = 1
    incrementor = 0.065
    randomIndex = random.randint(0,len(prob_list)-1) #interval: [0,9]
    while(resultIndex < 0):
        randomProbability = prob_list[randomIndex]
        if randomProbability > upperDouble:
            resultIndex = randomIndex
        else:
            randomIndex = random.randint(0,len(prob_list)-1) #interval: [0,9]
            upperDouble -= incrementor;
    return resultIndex

def probabilityCheck():
    sorted_testing_list = sorted(getSequenceList())
    prob_list = getProbList(sorted_testing_list)
    statistic_list = []
    sum_of_errors = 0
    for i in range(1000):
        statistic_list.append(getFittestIndex(sorted_testing_list))
    #results
    for i in range(len(prob_list)):
        print("No {0}, Occurances: {1}, Percentage: {2}".format(i, statistic_list.count(i), statistic_list.count(i)/10000.0))
        sum_of_errors += abs(statistic_list.count(i)/1000.0 - prob_list[i])
    for i in range(len(prob_list)):
        print("sequence no {0}, probability: {1}".format(i, prob_list[i]))
    #calculating avg error
    print("Average error:",sum_of_errors/len(prob_list))
    return sum_of_errors/len(prob_list)
