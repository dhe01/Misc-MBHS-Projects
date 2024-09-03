import random
import math
import numpy as np
import pandas as pd
import csv

# Read file
f = open("will.csv", "r")
state = []
office = []
bpi = []
polls = []
variance = []
stdev = []
numpolls = []
numpolls30 = []

a = 0
for i in f:
    if a == 0:
        pass
    else:
        row = i.split(",")
        state.append(row[0])
        office.append(row[1])
        bpi.append(float(row[2]))
        if row[3] == "NA":
            polls.append(float(row[2]))
        else:
            polls.append(float(row[3]))
        variance.append(float(row[4]))
        stdev.append(float(row[5]))
        numpolls.append(float(row[6]))
        numpolls30.append(float(row[7]))
    a += 1
f.close()

lean = []
for i in range(0, len(state)):
		weight = (1.72 / math.pi) * math.atan((0.6 * numpolls30[i] + 0.05 * numpolls[i]))
		counterweight = 1 - weight;
		combined = weight * polls[i] + counterweight * bpi[i];
		lean.append(combined)

correlated = []

# Correlation here
senate_seats = [36,29] #[dem, rep], number of sen seats not up for reelection
governorships = [6,8] #[dem, rep], number of gov seats not up for reelection

sen_races = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maryland', 'Missouri', 'Nevada', 'New Hampshire', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma_1', 'Oklahoma_2', 'Oregon', 'Pennsylvania', 'South Carolina', 'South Dakota', 'Utah', 'Vermont', 'Washington', 'Wisconsin']
gov_races = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Iowa', 'Kansas', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Nebraska', 'Nevada', 'New Hampshire', 'New Mexico', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Vermont', 'Wisconsin', 'Wyoming']
all = []
all_races = []
all = sen_races + gov_races
all.sort()
all_races = all

correlation_matrix = np.random.rand(71,71) #rand used only to create matrix

df = pd.read_csv("demographics z-scores.csv") #pulling sen race demographics from .csv data file

for j in range(len(correlation_matrix)): 
	for i in range(71):
		#print(all_races[j], all_races[i])
		if all_races[j] == all_races[i]:
			correlation_matrix[j, i] = 0.6
		else:
			race1 = df[all_races[j]]
			#print(race1)
			race2 = df[all_races[i]]
			#print(np.corrcoef(race1, race2))
			corrcoefs = np.corrcoef(race1, race2)
			#print(corrcoefs[1, 0])
			correlation_matrix[j, i] = corrcoefs[1, 0]
	

for j in range(len(correlation_matrix)): #prevent races from influencing their own results
    for i in range(71):
        if j==i:
            correlation_matrix[j,i] = 0

correlation_matrix[25,26] = 0.8 #setting the two OK races to same-state correlation value; review w/ cc
correlation_matrix[26,25] = 0.8

variance_data = pd.read_csv("will.csv")

variance_differences = np.random.rand(71,71) #differences between predicted and simulated result for each race due to normal variance, numpy just used to make matrix
#print(datafile.loc[0:1, "standard_deviation"])
for n in range(71):
    variance_differences[0, n] = (np.random.randn()*stdev[n])

correlation_effects = []
for n in range(71):
    correlation_effects.append(np.dot(variance_differences[0], correlation_matrix[n])/sum(correlation_matrix[n])) # dot product of differences and coefs divided by sum of coefs

for n in range(71):
	correlated.append(lean[n] + variance_differences[0:n] + correlation_effects[n])

# Run simulation
matrix = [[] for i in range(71)] # matrix with 71 rows with each row being a race 
runCount = 10000
counter = 0
while counter < runCount:
	runResult = []
	for i in range(0, len(state)):
		randomPoll = random.normalvariate(correlated[i], stdev[i])
		runResult.append(randomPoll)

	for i in range(0, len(matrix)):
		matrix[i].append(runResult[i])
	counter += 1

results = []
for i in range(0, len(matrix)):
	c = 0
	for j in range(0, len(matrix[i])):
		if matrix[i][j] > 50:
			c += 1
	results.append(100 * c / runCount)

g = open("output.csv", "w")
for i in range(0, len(results)):
    g.write(str(results[i]) + "\n")
g.close()
print("done")
