from timeit import default_timer as timer
from GeneticAlgoAPI.population import Population


def get_time_units(time):
    """ time is in seconds """
    unit = "seconds"
    if time <= 1e-1:
        time *= 1e3
        unit = "milliseconds"
    elif time > 60:
        time /= 60
        unit = "minutes"
        if time > 60:
            time /= 60
            unit = "hours"
    return time, unit


def evaluate(population, gen):
    fittest = population.get_fittest()
    f = fittest.get_fitness()
    # print("gen: {} fit: {} chromo: {}".format(str(gen), f, str(fittest)))


def run(ga, population):
    start = timer()

    ga.set_fitness_scores(population)
    gen = 0
    evaluate(population, gen)
    while not ga.get_stop_cond(population):
        gen += 1
        elite = ga.apply_elitism(population)
        parents = ga.selection(population)
        population = ga.crossover(parents, population.get_size())
        population = ga.mutation(population)
        population.add_chromosome(elite)
        ga.set_fitness_scores(population)

        evaluate(population, gen)

    end = timer()
    return end - start, population.get_fittest(), gen


def build_and_run(mutation_rate, crossover_rate, population_size, elitism_count, ga_type, chromo_type):
    ga = ga_type(elitism_count, mutation_rate, crossover_rate, population_size)
    population = Population()
    population.init_population(population_size, chromo_type)

    return run(ga, population)


