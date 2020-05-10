import csv

from main import main
from config import parameters

names = ["crossover","mutation", "elitism","population"]

def printToFile(CROSSOVER_RATE, MUTATION_RATE, ELITISM,POPULATION_SIZE, param:str, map:dict,gen = None, time = None):
    allParam = {names[0]: CROSSOVER_RATE, names[1]: MUTATION_RATE, names[2]: ELITISM,
                names[3]: POPULATION_SIZE}

    fileName = parameters.fileName
    if not fileName.endswith('.csv'):
        fileName += '.csv'
    with open(fileName, 'w', newline='') as csvfile:
        f = csv.writer(csvfile)  # , delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

        strParams = ' '.join('{}={}'.format(key, val) for key, val in allParam.items() if key != param)
        f.writerow([strParams])
        f.writerow("")
        f.writerow([param, ""] + list(map.keys()))
        f.writerow(["",""] + list(map.values()))
        f.writerow("")
        f.writerow("")
        f.writerow("")

def population(epochNum):
    parameters.fileName = "population_size"
    myMap = {}
    param = names[3]

    for jPOPULATION_SIZE in range(epochNum):
        parameters.POPULATION_SIZE = 20 + jPOPULATION_SIZE * 20
        meanTime = 0
        meanGen = 0
        epochForMean = 10
        for epoch in range(epochForMean):
            time, chromo, gen = main()

            meanGen += gen
            meanTime += time

        meanTime /= epochForMean
        meanGen /= epochForMean
        myMap[str(parameters.POPULATION_SIZE)] = "%.2f" % (meanGen * meanTime)
    print('25%')

    bestVal = min(myMap, key=myMap.get)

    printToFile(parameters.CROSSOVER_RATE, parameters.MUTATION_RATE, parameters.ELITISM, parameters.POPULATION_SIZE,
                param, myMap)  # gen = None, time = None), meanTime, meanGen)

    parameters.POPULATION_SIZE = int(bestVal)


def ELITISM(epochNum):
    parameters.fileName = "ELITISM_size"
    myMap = {}
    param = names[2]

    for jElitisim_SIZE in range(epochNum):
        parameters.ELITISM = jElitisim_SIZE
        meanTime = 0
        meanGen = 0
        epochForMean = 10
        for epoch in range(epochForMean):
            time, chromo, gen = main()

            meanGen += gen
            meanTime += time

        #meanTime /= epochForMean
        #meanGen /= epochForMean
        myMap[str(parameters.ELITISM)] = "%.2f" % (meanTime)
    print('50%')

    bestVal = min(myMap, key=myMap.get)

    printToFile(parameters.CROSSOVER_RATE, parameters.MUTATION_RATE, parameters.ELITISM, parameters.POPULATION_SIZE,
                param, myMap)  # gen = None, time = None), meanTime, meanGen)

    parameters.ELITISM = int(bestVal)


def mutation(epochNum):
    parameters.fileName = "mutation_size"
    myMap = {}
    param = names[1]

    for jMutation_SIZE in range(epochNum):
        parameters.MUTATION_RATE = jMutation_SIZE * 0.02
        meanTime = 0
        meanGen = 0
        epochForMean = 10
        for epoch in range(epochForMean):
            time, chromo, gen = main()

            meanGen += gen
            meanTime += time

        #meanTime /= epochForMean
        #meanGen /= epochForMean
        myMap[str(parameters.MUTATION_RATE)] = "%.2f" % (meanTime)
    print('75%')

    bestVal = min(myMap, key=myMap.get)

    printToFile(parameters.CROSSOVER_RATE, parameters.MUTATION_RATE, parameters.ELITISM, parameters.POPULATION_SIZE,
                param, myMap)  # gen = None, time = None), meanTime, meanGen)

    parameters.MUTATION_RATE = float(bestVal)



def crossover(epochNum):
    parameters.fileName = "crossover_size"
    myMap = {}
    param = names[0]

    for jCrossover_SIZE in range(epochNum):
        parameters.CROSSOVER_RATE = 0.01 + jCrossover_SIZE * 0.02
        meanTime = 0
        meanGen = 0
        epochForMean = 10
        for epoch in range(epochForMean):
            time, chromo, gen = main()

            meanGen += gen
            meanTime += time

        #meanTime /= epochForMean
        #meanGen /= epochForMean
        myMap[str(parameters.CROSSOVER_RATE)] = "%.2f" % (meanTime)
    print('100%')

    bestVal = min(myMap, key=myMap.get)

    printToFile(parameters.CROSSOVER_RATE, parameters.MUTATION_RATE, parameters.ELITISM, parameters.POPULATION_SIZE,
                param, myMap)  # gen = None, time = None), meanTime, meanGen)

    parameters.CROSSOVER_RATE = float(bestVal)








if __name__ == '__main__':
    # init first args.
    parameters.POPULATION_SIZE = 120
    parameters.ELITISM = 3
    parameters.MUTATION_RATE = .06
    parameters.CROSSOVER_RATE = .88
    epochNum = 50

    population(epochNum)
    if (parameters.POPULATION_SIZE > 200):
        ELITISM(epochNum)
    elif parameters.POPULATION_SIZE < 25:
        ELITISM(parameters.POPULATION_SIZE)
    else:
        ELITISM(25)

    mutation(25)
    crossover(46)
