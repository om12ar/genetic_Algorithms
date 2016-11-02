import random
from datetime import datetime

pop_size = 70
max_generations = 300
probability_of_crossover = 0.5
probability_of_mutation = 0.1

optimal_phenome = -100
optimal_genome = ""


def initiate(pop, num_of_items):
    for i in range(0, pop_size):
        chromosome = ""
        for j in range(0, num_of_items):
            if random.uniform(0, 1) < 0.5:
                chromosome += "0"
            else:
                chromosome += "1"
        pop.append(chromosome)


def evaluate_fitness(chromosome, items, sack_size):
    ss = int(sack_size)
    i = 0
    benefit = 0
    for c in chromosome:
        gene = int(c)
        if gene == 1:
            ss -= items[i][0]
            if ss < 0:
                return -1
            benefit += items[i][1]
        i += 1

    return benefit


def get_probability(fitnesses):
    cumulative_probability = [0]
    for fitness in fitnesses:
        cumulative_probability.append(cumulative_probability[-1] + fitness)
    cumulative_probability.remove(0)
    return cumulative_probability


def select_pair(cumulative_probability, population):
    pair = []
    for i in range(0, 2):
        prop = random.uniform(0, cumulative_probability[-1])
        index = 0
        for p in cumulative_probability:
            if prop <= p:
                pair.append(population[index])
                break
            index += 1

    return pair


def cross_over(selected_pair, num_of_items):
    global probability_of_crossover
    PC = random.uniform(0, 1)
    if PC < probability_of_crossover:
        return selected_pair

    split_point = int(random.uniform(1, num_of_items - 1))
    new_pair = []
    parent1 = selected_pair[0]
    parent2 = selected_pair[1]
    new_pair.append(parent1[0:split_point] + parent2[split_point:])
    new_pair.append(parent2[0:split_point] + parent1[split_point:])
    return new_pair


def mutate(cross_over_pair):
    global probability_of_mutation
    mutate_pair = []
    for kid in cross_over_pair:
        for idx, i in enumerate(kid):
            Pm = random.uniform(0, 1)
            if Pm <= probability_of_mutation:
                if kid[idx] == "0":
                    kid = kid[:idx] + "1" + kid[idx + 1:]
                else:
                    kid = kid[:idx] + "0" + kid[idx + 1:]
        mutate_pair.append(kid)
    return mutate_pair


def get_optimal(chromosome, fitness):
    global optimal_phenome
    global optimal_genome
    if fitness > optimal_phenome:
        optimal_phenome = fitness
        optimal_genome = chromosome


def replace_infeasible(number, num_of_items, items, sack_size):
    newChromo = []
    for i in range(0, number):

        while True:
            chromosome = ""
            for j in range(0, num_of_items):
                if random.uniform(0, 1) < 0.5:
                    chromosome += "0"
                else:
                    chromosome += "1"

            if evaluate_fitness(chromosome, items, sack_size) != -1:
                break
        newChromo.append(chromosome)
    return newChromo


def main():
    num_of_test = int(input())
    global optimal_phenome
    global optimal_genome
    # skip a line
    input()
    for t in range(0, num_of_test):

        optimal_phenome = -100
        optimal_genome = ""
        num_of_items = int(input())
        sack_size = int(input())
        items = []
        for i in range(0, num_of_items):
            the_string = input()
            x, y = the_string.split()
            item_pair = [int(x), int(y)]
            items.append(item_pair)

        population = []
        initiate(population, num_of_items)

        global pop_size
        for gen in range(0, max_generations):

            # remove -1
            population = [item for item in population if evaluate_fitness(item, items, sack_size) != -1]
            population += replace_infeasible(pop_size - len(population), num_of_items, items, sack_size)

            fitnesses = []
            for chromosome in population:
                fitness = evaluate_fitness(chromosome, items, sack_size)
                get_optimal(chromosome, fitness)
                fitnesses.append(fitness)
            cumulative_probability = get_probability(fitnesses)
            new_population = []

            for i in range(0, int(pop_size / 2)):
                selected_pair = select_pair(cumulative_probability, population)
                cross_over_pair = cross_over(selected_pair, num_of_items)
                mutant = mutate(cross_over_pair, num_of_items)
                new_population.append(mutant[0])
                new_population.append(mutant[1])

            population = new_population

        print("case", t + 1, ":", optimal_phenome)
        print(optimal_genome)
        # skip a line
        input()

random.seed(datetime.now())
main()
