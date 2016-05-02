#phase1-processed
import pprint, tarjan
fileName = "SAMPLEINSTANCE"
#adding these lines
import networkx as nx
from collections import defaultdict
from JohnsonsAlgo import simple_cycles
import operator

dct = {}
children = []

"""Function to return list of optimal, approximated cycles for a particular input file.
The input is a string e.g. '42' which is a repr of 42.in in the phase1-processed directory"""
def calcCycles(inputFileNumber):
	#Opening
	global dct
	global children #I added this

	f = open("phase1-processed/" + inputFileNumber + ".in", "r")
	numNodes = f.readline().split()
	numNodes = int(numNodes[0])
	print('numNodes ' + str(numNodes))	

	#Reading indices of children
	readInChildren = f.readline().split()
	children = ''.join(readInChildren)
	childPenaltyUpperBound = 2 * len(children)
	if children in ['/n', '\r\n', ""]:
		children = []
	else:
		children = readInChildren

	#Total possible penalty = 2 * child vertices + 
	#Calculating total possible penality as a baseline comparison
	totalPenalty = childPenaltyUpperBound #TODO: add num of non-child nodes
	print "TOTAL POSSIBLE PENALTY", totalPenalty



	dct = {}



	#Creating dictionary representation to pass into tarjan library
	for i in xrange(numNodes):
		line = f.readline().split()
		for j in xrange(numNodes):
			if int(line[j]) == 1:
				# if the node is already in the dictionary, extend its list of edges to include edge j
				if i in dct:
					current_edges = dct[i]
					current_edges.append(j)
				#if the node is not yet in the dictionary, add key i and value [j]
				else:
					dct[i] = [j]

	listOfSCC = tarjan.tarjan(dct)
		
	#remove all SCCs of length 1 or less
	for scc in listOfSCC:
		if len(scc) < 2:
			listOfSCC.remove(scc)

		
	print "\n SCCS for file: ", fileName, ": ", listOfSCC
		# print "dictionary : ", dct


#Do calculations for each file in dir
#TODO: map the cycles ouputted to each file to a newline in finaloutput.out
calcCycles(fileName)


""""Take dct initialized by calcCycles() and
	turn it into edges representation of the 
	graph. Write edges into edges.txt file as
	an input file of Johnson's algorithm."""
def dctToEdges():
	inputString = ""
	for key in dct:
		for value in dct[key]:
			inputString = inputString + str(key) + " " + str(value) + "\n"
			# print str(key) + " " + str(value) + "\n"
	# print inputString

	f = open("edges.txt", "w")
	f.write(inputString)
	f.close()

dctToEdges()






#Run Johnson's Algorithm within input_reader
#for now, will return a list of the optimal cycles given by the greedy algorithm

G = nx.DiGraph()


# create G
inputf = open("edges.txt", "r")
for edge in inputf.readlines():
    v1,v2 = edge.split(' ', 1)
    G.add_edge(v1.strip(),v2.strip())

#put all possible cycles of length 5 or smaller in a list
simple_sol = []
for c in simple_cycles(G):
    if len(c) <= 6 :
    	simple_sol.append(c[:-1])

#make a dictionary with key: index of cycle in simple_sol, value: score for the cycle
cycle_and_score = {}

for index, cycle in enumerate(simple_sol):
	score = 0
	for elem in cycle:
		# + 2 for children
		if elem in children:
			score += 2
		# + 1 for non - children
		else:
			score += 1
	cycle_and_score[index] = score

#greedily choose the cycles of highest score as the output, making sure all cycles are disjoint
restricted_vertices = []
solution = []

while cycle_and_score:
	max_val_cycle_index = max(cycle_and_score.iteritems(), key=operator.itemgetter(1))[0]
	max_val_cycle = simple_sol[max_val_cycle_index]
	can_add = True
	for node in max_val_cycle:
		if node in restricted_vertices:
			can_add = False
			del cycle_and_score[max_val_cycle_index]
			break
	if can_add:
		solution.append(max_val_cycle)
		restricted_vertices.extend(max_val_cycle)
		del cycle_and_score[max_val_cycle_index]


print "simple solution not considering disjoint cycles was ", simple_sol
print "after greedily choosing disjoint cycles, solution is ", solution


# print simple_cycles(G)
#outputf = open("possibleCycles.txt", "w")
#for c in simple_cycles(G):
#    if len(c) <= 6 :
#        outputf.write(" ".join(c[:-1]) + "\n\n")
#outputf.close()


# for i in range(0, len(d)):
# 	for j in range(0,len(d[0])):
# 		print "d at: ", i, " ", j, " ", d[i][j]

#create 2D array logic
# d = [[0 for j in range(numNodes)] for i in range(numNodes)]



# for i in xrange(numNodes):
# 	line = f.readline().split()
# 	#checks each value is an int
# 	for j in xrange(numNodes):

# 		if not line[j].isdigit():
# 			print "Line " + str(i+2) + " must contain numNodes integers."
# 		d[i][j] = int(line[j])
# 		# if d[i][j] < 0 or d[i][j] > 1:
# 		# 	return "The adjacency matrix must be comprised of 0s and 1s."

# # for i in xrange(numNodes):
# # 	if d[i][i] != 0:
# # 		return "A node cannot have an edge to itself."


