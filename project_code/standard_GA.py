#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

#Modified by Grant Nike 6349302
#Cosc 4P82 Final Project

from asyncio import futures
import operator
import math
import random
import itertools
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from datetime import datetime
import sys
from pathlib import Path

#Open parameter file to read in parameters
if len(sys.argv) > 1:
    path = sys.argv[1]
    param_file = open("parameters/"+path,"r")
    if len(sys.argv) > 3:
        run = int(sys.argv[3])
else:
    param_file = open("parameters.txt","r")
params = param_file.read()
ls = params.split("\n")
input_file = ls[0]
#Number of generations to run GP for
generations = int(ls[1])
#Population Size
population = int(ls[2])
#Crossover probability
crossover_percent = float(ls[3])
#Mutation probability
mutation_percent = float(ls[4])
#Percentage of data to be used as training data, rest is testing data
data_split = float(ls[5])
param_file.close()

#Reads points from a text file
rows = 351
columns = 34 #Last column is just an id, second last is quality rating
data = [[0 for i in range(columns)] for j in range(rows)]
answers = []
data_file = open(input_file,"r")
#first_line = data_file.readline() #Skip first line, as it is just column labels
for n in range(rows):
    line = data_file.readline()
    line = line.split(",")
    #Add wine quality answers for fitness checks
    answers.append(line[columns].strip('\n'))
    for k in range(columns):
        #Add all data except last two attributes
        data[n][k] = float(line[k])

#Shuffle data and answers using Fisher-Yates shuffle algorithm
random.seed(datetime.now().microsecond)
for i in range(len(data)-1,0,-1):
    #random index in array from 0 to i
    j = random.randint(0,i+1)
    #swap arr i with arr j
    data[i], data[j] = data[j], data[i]
    answers[i], answers[j] = answers[j], answers[i]

#split data into training and testing sets
training_data = []
training_answers = []
testing_data = []
testing_answers = []
for i in range(rows):
    if i < data_split*rows:
        training_data.append(data[i])
        training_answers.append(answers[i])
    else:
        testing_data.append(data[i])
        testing_answers.append(answers[i])

#Strongly typed GP language
pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float,columns), float)

#Safe division function
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1
#Arithmetic Operators
pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)
pset.addPrimitive(min, [float,float], float)
pset.addPrimitive(max, [float,float], float)
pset.addPrimitive(operator.neg, [float], float)
# pset.addPrimitive(math.cos, [float], float)
# pset.addPrimitive(math.sin, [float], float)

#Define if_else operator
def if_else(input,first,second):
    if input: return first
    else: return second
#Boolean operators
# pset.addPrimitive(operator.lt,[float,float],bool)
# pset.addPrimitive(operator.eq,[float,float],bool)
# pset.addPrimitive(if_else,[bool,float,float],float)
#Terminals
pset.addEphemeralConstant("rand100",lambda: random.random()*10,float)
# pset.addTerminal(False,bool)
# pset.addTerminal(True,bool)
pset.renameArguments(ARG0='x')


#Maximizing fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def hit_check(value, answer):
    if value >= 0.0 and answer == 'g':
        return 1
    elif value < 0.0 and answer == 'b':
        return 1
    return 0

def evalTraining(individual, training_data, training_answers):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    #Evaluate fitness
    hits = 0
    for i in range(len(training_data)):
        value = func(*training_data[i][:columns])
        hits += hit_check(value,training_answers[i])
    hits = hits/math.floor(data_split*rows)

    fit = []
    fit.append(hits)
    return fit

toolbox.register("evaluate", evalTraining, training_data=training_data,training_answers=training_answers)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    #There will be a different random seed everytime, as the seed is the current time in milliseconds
    random.seed(datetime.now().microsecond)
    #Initialize population
    pop = toolbox.population(n=population)
    #Save single best answer for run
    hof = tools.HallOfFame(1)
    
    #Set up log stats
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    
    #Run basic evolutionary algorithm 
    pop, log = algorithms.eaSimple(pop, toolbox, crossover_percent, mutation_percent, generations, stats=mstats,
                                   halloffame=hof, verbose=True)
    
    #Run best evolved answer on test set
    best = toolbox.compile(expr=hof[0])
    fit = 0
    for i in range(len(testing_data)):
        value = best(*testing_data[i][:columns])
        fit += hit_check(value,testing_answers[i])
    fit = fit / len(testing_data)
    
    #Print log and other run info to terminal
    best = f"\n Best Answer of run: {hof[0]}"
    print (best)
    tested_fit = f"\n Fitness on testing data: {fit}"
    print(tested_fit)
    fit_max = log.chapters["fitness"].select("max")
    fit_avg = log.chapters["fitness"].select("avg")
    #Output log to data file
    if len(sys.argv) > 3:
        output_file = sys.argv[2]
        data_file = open(output_file+f"/output_run{run}.txt","w",encoding="utf-8")
    else:
        output_file = "output.txt"
        data_file = open(output_file,"w",encoding="utf-8")
    data_file.write(str(fit_max)+"\n")
    data_file.write(str(fit_avg)+"\n")
    data_file.write(str(fit))
    data_file.write(best)
    data_file.close()
    
    return pop, log, hof

if __name__ == "__main__":
    main()