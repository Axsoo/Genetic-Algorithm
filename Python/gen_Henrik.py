import random
import math

class Population():
    def __init__(self, population_size, n_arr):
        self.population_array = self.generatePopulation(population_size)
        self.n_arr = n_arr
        self.p_c = 0.6
        self.p_m = 0.002

    def generatePopulation(self, population_size):
        population_output = []

        for i in range(0, population_size):
            population_output.append(Chromosome(genBinSeq()))

        return population_output

    def evolve(self):
        new_population = []

        while len(new_population) < len(self.population_array):
            selected_chromosome_1 = self.select()
            selected_chromosome_2 = self.select()
            chromosome_1 = selected_chromosome_1
            chromosome_2 = selected_chromosome_2

            if random.random() <= self.p_c:
                cut_index = random.randint(1, len(self.n_arr))
                chromosome_1 = self.crossover(selected_chromosome_1.bin_seq, selected_chromosome_2.bin_seq, cut_index)
                chromosome_2 = self.crossover(selected_chromosome_2.bin_seq, selected_chromosome_1.bin_seq, cut_index)

            chromosome_1.mutate(self.p_m)
            chromosome_2.mutate(self.p_m)

            new_population.append(chromosome_1)
            new_population.append(chromosome_2)

        self.population_array = new_population

    def crossover(self, chr1, chr2, cut_index):
        part_1 = chr1[0:cut_index]
        part_2 = chr1[cut_index:]
        return Chromosome(part_1 + part_2)

    def select(self):
        total_fitness = 0
        cumulative_fitness = []

        for i in range(0, len(self.population_array)):
            current_fitness = self.population_array[i].getFitness(self.n_arr, 38, 210)
            total_fitness += current_fitness
            cumulative_fitness.append(total_fitness)
            if current_fitness == 1:
                print("Solution found: " + self.population_array[i].bin_seq)
                quit()

        random_value = random.uniform(0, total_fitness)

        for i in range(0, len(self.population_array)):
            if random_value <= cumulative_fitness[i]:
                return self.population_array[i]

        return self.population_array[-1]

    def show(self):
        for current_chromosome in self.population_array:
            print(current_chromosome.bin_seq)
            print(current_chromosome.getFitness(self.n_arr, 38, 210))

class Chromosome():
    def __init__(self, data):
        self.bin_seq = data

    def getFitness(self, n_arr, ideal_sum, ideal_product):
        sum = 0
        product = 1

        for i in range(0, len(n_arr)):
            if self.bin_seq[i] == '0':
                sum += n_arr[i]
            else:
                product *= n_arr[i]

        fitness = 1 / (1 + (math.sqrt(1 * ((sum - ideal_sum) ** 2) + (0.01 * (product - ideal_product) ** 2))))

        return fitness

    def mutate(self, p_m):
        new_bin = ""
        for i in range(0, len(self.bin_seq)):
            if random.random() <= p_m:
                if self.bin_seq[i] == '0':
                    new_bin += '1'
                else:
                    new_bin += '0'
            else:
                new_bin += self.bin_seq[i]

        self.bin_seq = new_bin

def genBinSeq():
    bin_output = ""
    for i in range(0, 10):
        bin_output += str(random.randint(0,1))

    return bin_output


def main():
    n_arr = list(range(1, 11))
    pop = Population(100, n_arr)
    #pop.show()
    select = []
    for i in range(0, 100):
        select.append(str(pop.select().bin_seq))
        print(select[i])
    #pop.show()

if __name__ == '__main__':
    main()
