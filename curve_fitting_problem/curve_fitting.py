import random
from datetime import datetime

pop_size = 100
max_generations = 100
probability_of_crossover = 0.5
probability_of_mutation = 0.2

optimal_phenome = float("inf")
optimal_genome = []


def get_optimal(chromosome, fitness):
    global optimal_phenome
    global optimal_genome
    if fitness < optimal_phenome:
        optimal_phenome = fitness
        optimal_genome = chromosome


def initiate(pop, degree):
    for i in range(0, pop_size):
        chromosome = []
        for j in range(0, degree + 1):
            chromosome.append(round(random.uniform(-10, 10), 1))

        pop.append(chromosome)


def evaluate_fitness(chromosome, points):
    mean_square_error = 0.0

    for point in points:
        y = 0
        for i, coeff in enumerate(chromosome):
            y += coeff * pow(point[0], i)
        mean_square_error += pow(y - point[1], 2)

    mean_square_error *= (1 / len(points))
    return mean_square_error


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


def cross_over(selected_pair, degree):
    global probability_of_crossover
    if random.uniform(0, 1) < probability_of_crossover:
        return selected_pair

    split_point = int(random.uniform(1, degree + 1))
    new_pair = []
    parent1 = selected_pair[0]
    parent2 = selected_pair[1]
    new_pair.append(parent1[0:split_point] + parent2[split_point:])
    new_pair.append(parent2[0:split_point] + parent1[split_point:])
    return new_pair


def mutate(chromosome, current_gen):
    global probability_of_mutation
    dependency = 2.75
    index = 0
    for gene in chromosome:
        if random.uniform(0, 1) <= probability_of_mutation:
            low_delta = -10 - gene
            high_delta = 10 - gene
            selected_delta = 0
            r = random.uniform(0, 1)

            if r <= 0.5:
                selected_delta = low_delta
            else:
                selected_delta = high_delta

            amount_of_mutation = selected_delta * (1 - pow(r, pow(1 - (current_gen / max_generations), dependency)))
            gene += amount_of_mutation
            chromosome[index] = gene
            index += 1
    return chromosome


def main():
    num_of_test = int(input())
    global optimal_phenome
    global optimal_genome

    for t in range(0, num_of_test):

        optimal_phenome = float("inf")
        optimal_genome = []

        the_string = input()
        x, y = the_string.split()
        num_of_points = int(x)
        degree = int(y)
        points = []
        for i in range(0, num_of_points):
            the_string = input()
            x, y = the_string.split()
            coordinates = [float(x), float(y)]

            points.append(coordinates)

        population = []
        initiate(population, degree)
        global pop_size
        for gen in range(0, max_generations):
            fitnesses = []
            for chromosome in population:
                fitness = evaluate_fitness(chromosome, points)
                get_optimal(chromosome, fitness)
                fitnesses.append(fitness)
            cumulative_probability = get_probability(fitnesses)
            new_population = []
            for i in range(0, int(pop_size / 2)):
                selected_pair = select_pair(cumulative_probability, population)
                cross_over_pair = cross_over(selected_pair, degree)
                new_population.append(mutate(cross_over_pair[0], gen))
                new_population.append(mutate(cross_over_pair[1], gen))
            population = new_population

        print("case : ", t + 1)
        print("Optimal Genome: ", optimal_genome)
        print("Optimal Phenome: ", optimal_phenome)

random.seed(datetime.now())
main()
