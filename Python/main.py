import random
import numpy as np
import matplotlib.pyplot as plt

#
# global constants
ORIGINAL_LIST = [1,2,3,4,5,6,7,8,9,10]
IDEAL_SUM = 38 #default: 38
IDEAL_PRODUCT = 210 #default: 210
SEQUENCE_SIZE = 10 #default: 10
POPULATION_SIZE = 100 #default: 100
NUMBER_OF_GENERATIONS = 100 #default: 100
MUTATION_RATE = 1 #max 1000
CROSSOVER_RATE = 100 #max 100

#
# functions
def getBinarySequence(length): #ok
    binaryString = ""
    for i in range(length):
            binaryString += str(random.randint(0,1))
    return binaryString

def getSumProduct(sequence):
    sum = 0
    product = 1
    for i in range(len(sequence)):
        if sequence[i] == '0':
            sum += ORIGINAL_LIST[i]
            #print("Index no {0} is a 0, which corresponds to {1}".format(i,ORIGINAL_LIST[i]))
        elif sequence[i] == '1':
            product *= ORIGINAL_LIST[i]
            #print("Index no {0} is a 1, which corresponds to {1}".format(i,ORIGINAL_LIST[i]))
    return (sum, product)

def getFitness(sequence):
    return 1 /(((getSumProduct(sequence)[0] - IDEAL_SUM)**2 + ((getSumProduct(sequence)[1]) - IDEAL_PRODUCT)**2)**0.5 + 1)

def getSequenceList():
    sequence_list = []
    for i in range(POPULATION_SIZE):
        sequence = getBinarySequence(SEQUENCE_SIZE)
        sequence_list.append([getFitness(sequence), sequence])
    return sequence_list

def printList(listIn):
    prob_list = getProbList(listIn)
    for i in range(len(listIn)):
        print("seq: {0}, fit: {1}, chance: {2}%".format(listIn[i][1], listIn[i][0], round(100 * prob_list[i])))
    #print("Average getFitness:",getAverageFitness(listIn))
    print("Highest fitness:",max(listIn))
    x_data = []
    y_data = []
    listIn = sorted(listIn)
    for i in range(len(listIn)):
        x_data.append(i)
        y_data.append(listIn[i][0])
    #scatterplot(x_data, y_data)

def scatterplot(x_data, y_data, x_label="", y_label="", title="", color="r", yscale_log="True"):
    #Create plot object
    _, ax = plt.subplots()
    ax.scatter(x_data, y_data,s = 10, color = color, alpha = 0.75)
    ax.set_title("Fitness by index")
    ax.set_xlabel("Index")
    ax.set_ylabel("Fitness")
    plt.show()


def getAverageFitness(listIn):
    sum = 0
    for i in range(len(listIn)):
        sum += listIn[i][0]
    return sum/len(listIn)

def getProbList(listIn):
    sum_of_fitnesses = 0
    for i in range(len(listIn)):
        sum_of_fitnesses += listIn[i][0]
    prob_list = []
    for i in range(len(listIn)):
        prob_list.append(listIn[i][0] / sum_of_fitnesses)
    return prob_list

def getFittestIndex(sorted_list):
    prob_list = getProbList(sorted_list)
    random_num = random.random()
    lower_bound = 0
    upper_bound = 0
    for i in range(len(sorted_list)):
        if i == 0:
            lower_bound = 0
            upper_bound = prob_list[0]
        else:
            lower_bound += prob_list[i-1]
            upper_bound += prob_list[i]
        if(lower_bound < random_num) and (random_num < upper_bound):
            #print("Fittest index was no {0}, with a probability of {1}%".format(i,round(prob_list[i]*100)))
            return i

def mutate(binaryString):
    #print("Mutation occured!")
    lst = list(binaryString)
    for i in range(len(lst)-1):
        if random.randint(0,1000) < MUTATION_RATE:
            if lst[i] == '1':
                lst[i] = '0'
            else:
                lst[i] = '1'
    returnString = ""
    for char in lst: returnString += char
    return returnString

def crossoverEpisode(sequence1, sequence2):
    randomIndex = random.randint(1,len(sequence1)-1)
    new_sequence1 = sequence1[:randomIndex] + sequence2[randomIndex:]
    new_sequence2 = sequence2[:randomIndex] + sequence1[randomIndex:]
    new_sequence1 = mutate(new_sequence1)
    new_sequence2 = mutate(new_sequence2)
    return ([getFitness(new_sequence1), new_sequence1], [getFitness(new_sequence2), new_sequence2])

def main():

    current_pop = getSequenceList()
    new_pop = []
    #Gen 0
    generation = 0
    printList(current_pop)
    print("Generation:",generation,'\n')
    input("Start loop?")
    #Generation loop
    while(generation < NUMBER_OF_GENERATIONS):
        generation += 1
        fittest_pool = [] #here we put the selected binSeqs from which we build the new population
        for i in range(0,int(POPULATION_SIZE)):
            fittest_pool.append(current_pop[getFittestIndex(current_pop)][1]) #pool same size as pop
        for i in range(0,int(POPULATION_SIZE/2)):
            bestSeq1 = fittest_pool[random.randint(0,len(fittest_pool)-1)]
            bestSeq2 = fittest_pool[random.randint(0,len(fittest_pool)-1)]
            while(bestSeq1 == bestSeq2):
                #print("Picked the same!")
                bestSeq2 = fittest_pool[random.randint(0,len(fittest_pool)-1)]
            if random.randint(0,100) < CROSSOVER_RATE:
                (newSeq1, newSeq2) = crossoverEpisode(bestSeq1, bestSeq2)
                #print(bestSeq1,"and",bestSeq2,"becomes",newSeq1,"and",newSeq2)
            else:
                newSeq1 = [getFitness(bestSeq1), bestSeq1]
                newSeq2 = [getFitness(bestSeq2), bestSeq2]
            new_pop.append(newSeq1)
            new_pop.append(newSeq2)
        printList(new_pop)
        print("Generation:",generation,'\n')
        current_pop = new_pop.copy()
        new_pop = []
        if generation % 1 == 0:
            x = input("Continue?")
            if x == 'no':
                break

if __name__ == '__main__':
    main()
