#Grant Nike 6349302
#COSC 4P82 Assignment #1
#Plots data from experiments using matplot


import numpy
import sys
import matplotlib.pyplot as plt

gens = 50
runs = 10
gen = [i for i in range(gens)]

avg_max_test1 = numpy.array([0 for i in range(gens)])
avg_test1 = numpy.array([0 for i in range(gens)])
testing_avg1 = 0
for run in range(1,11):
    input = open(f"output1/output_run{run}.txt")
    
    min_fit = input.readline()
    min_fit = min_fit.strip("[")
    min_fit = min_fit.strip("]")
    min_fit = min_fit.strip("\n")
    min_fit = min_fit.split(",")
    for i in range(len(min_fit)):
        min_fit[i] = float(min_fit[i].strip("]"))
    if len(min_fit) == 51:
        min_fit = min_fit[1:]
    avg_max_test1 = avg_max_test1 + min_fit
    
    avg_fit = input.readline()
    avg_fit = avg_fit.strip("[")
    avg_fit = avg_fit.strip("]")
    avg_fit = avg_fit.strip("\n")
    avg_fit = avg_fit.split(",")
    for i in range(len(avg_fit)):
        avg_fit[i] = float(avg_fit[i].strip("]"))
    if len(avg_fit) == 51:
        avg_fit = avg_fit[1:]
    avg_test1 = avg_test1 + avg_fit
    
    testing_avg1 += float(input.readline().strip('\n'))
    
    input.close()
avg_max_test1 = avg_max_test1/runs
avg_test1 = avg_test1/runs
testing_avg1 = testing_avg1/runs

avg_max_test2 = numpy.array([0 for i in range(gens)])
avg_test2 = numpy.array([0 for i in range(gens)])
testing_avg2 = 0
for run in range(1,11):
    input = open(f"output2/output_run{run}.txt")
    
    min_fit = input.readline()
    min_fit = min_fit.strip("[")
    min_fit = min_fit.strip("]")
    min_fit = min_fit.strip("\n")
    min_fit = min_fit.split(",")
    for i in range(len(min_fit)):
        min_fit[i] = float(min_fit[i].strip("]"))
    if len(min_fit) == 51:
        min_fit = min_fit[1:]
    avg_max_test2 = avg_max_test2 + min_fit
    
    avg_fit = input.readline()
    avg_fit = avg_fit.strip("[")
    avg_fit = avg_fit.strip("]")
    avg_fit = avg_fit.strip("\n")
    avg_fit = avg_fit.split(",")
    for i in range(len(avg_fit)):
        avg_fit[i] = float(avg_fit[i].strip("]"))
    if len(avg_fit) == 51:
        avg_fit = avg_fit[1:]
    avg_test2 = avg_test2 + avg_fit
    testing_avg2 += float(input.readline().strip('\n'))
    
    input.close()
avg_max_test2 = avg_max_test2/runs
avg_test2 = avg_test2/runs
testing_avg2 = testing_avg2/runs

fig, ax1 = plt.subplots()
line1 = ax1.plot(gen, avg_max_test1, "b-", label="Max Fitness Test 1")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Max Fitness")
for tl in ax1.get_yticklabels():
    tl.set_color("b")

#ax2 = ax1.twinx()
line2 = ax1.plot(gen, avg_max_test2, "r-", label="Max Fitness Test 2")
for tl in ax1.get_yticklabels():
    tl.set_color("r")
    
lns = line1 + line2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc="center right")

plt.show()


fig, ax1 = plt.subplots()
line1 = ax1.plot(gen, avg_test1, "b-", label="Average Fitness Test 1")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Average Fitness")
for tl in ax1.get_yticklabels():
    tl.set_color("b")

#ax2 = ax1.twinx()
line2 = ax1.plot(gen, avg_test2, "r-", label="Average Fitness Test 2")
for tl in ax1.get_yticklabels():
    tl.set_color("r")
    
lns = line1 + line2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc="center right")

plt.show()

output = open("average_output.txt","w")
output.write(f"Average fitness on testing data for parameters1: {testing_avg1}\n")
output.write(f"Average fitness on testing data for parameters2: {testing_avg2}\n")
output.write("\n")
for elem in avg_max_test1:
    output.write(str(elem)+"\n")
output.write("avg_max_test1"+"\n")
for elem in avg_max_test2:
    output.write(str(elem)+"\n")
output.write("avg_max_test2"+"\n")
for elem in avg_test1:
    output.write(str(elem)+"\n")
output.write("avg_test1"+"\n")
for elem in avg_test2:
    output.write(str(elem)+"\n")
output.write("avg_test2"+"\n")