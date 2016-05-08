import pprint, tarjan
import networkx as nx
import operator
from collections import Counter

fileName = "SAMPLEINSTANCE"
# dct = {}
children = []
# listOfSCC = []
adjaMatrix = []
edges = []
cycles = []
numNodes = 0
G = None
# ratio = []

"""Function to return list of optimal, approximated cycles for a particular input file.
The input is a string e.g. '42' which is a repr of 42.in in the phase1-processed directory"""
def initializeAM(inputFileNumber):
	#Opening
	# global dct
	global children #I added this
	# global listOfSCC
	global adjaMatrix
	global numNodes

	f = open("phase1-processed/" + inputFileNumber + ".in", "r")
	numNodes = f.readline().split()
	numNodes = int(numNodes[0])
	# print('numNodes ' + str(numNodes))	

	#Reading indices of children
	readInChildren = f.readline().split()
	children = ''.join(readInChildren)
	childPenaltyUpperBound = 2 * len(children)
	if children in ['/n', '\r\n', ""]:
		children = []
	else:
		children = map(int, readInChildren)

	#Total possible penalty = 2 * child vertices + 1 * adult vertices
	#Calculating total possible penality as a baseline comparison
	totalPenalty = childPenaltyUpperBound + numNodes - len(children)
	# print "TOTAL POSSIBLE PENALTY", totalPenalty

	# dct = {}
	adjaMatrix = []
	#Creating dictionary representation to pass into tarjan library
	for i in xrange(numNodes):
		line = map(int, f.readline().split())
		adjaMatrix.append(line)

	# 	for j in xrange(numNodes):
	# 		if int(line[j]) == 1:
	# 			# if the node is already in the dictionary, extend its list of edges to include edge j
	# 			if i in dct:
	# 				current_edges = dct[i]
	# 				current_edges.append(j)
	# 			#if the node is not yet in the dictionary, add key i and value [j]
	# 			else:
	# 				dct[i] = [j]
	# listOfSCC = tarjan.tarjan(dct)


def convertToEdges():
	global edges
	edges = []
	for row in xrange(numNodes):
		for col in xrange(numNodes):
			if adjaMatrix[row][col] == 1:
				edges.append((row, col))

# Find all the simple unique cycles
def simpleCycles():
	global cycles
	global G
	# global ratio
	G = nx.DiGraph()
	G.add_edges_from(edges)

	nodes = []
	for i, j in edges:
		if i not in nodes:
			nodes.append(i)
	for i in nodes:
		for n in xrange(1, 5):
			cycles.extend([path for path in findPaths(G, i, n) if i in G.neighbors(path[-1])])
	
	removeDuplicateCycles()

# Remove duplicate cycles
def removeDuplicateCycles():
	global cycles
	for cycle in cycles:
		cycle.sort()
	cycles.sort()

	uniqueCycles = [[1]]
	for cycle in cycles:
		if cycle != uniqueCycles[-1]:
			uniqueCycles.append(cycle)
	cycles = uniqueCycles[1:]


# restore the nodes' order such that they form a cycle
def cycleConstructor(ls_between, start, end):
	global G

	if len(ls_between) == 1:
		if ls_between[0] in G.neighbors(start) and end in G.neighbors(ls_between[0]): 
			return ls_between + [end]
		else:
			return []
	for node in ls_between:
		if node in G.neighbors(start):
			index = ls_between.index(node)
			tmp = ls_between[0]
			ls_between[0] = node
			ls_between[index] = tmp
			cycle =  [node] + cycleConstructor(ls_between[1:], node, end)
			if len(cycle) == len(ls_between) + 1:
				return cycle
	return []


def findPaths(G,u,n,excludeSet = None):
	if excludeSet == None:
		excludeSet = set([u])
	else:
		excludeSet.add(u)
	if n == 0:
		return [[u]]
	paths = [[u]+path for neighbor in G.neighbors(u) if neighbor not in excludeSet for path in findPaths(G,neighbor,n-1,excludeSet)]
	excludeSet.remove(u)
	return paths


def solutionCycles():

	cycle_and_score = {}
	for index, cycle in enumerate(cycles):
		score = 0
		for elem in cycle:
			# + 2 for children
			if elem in children:
				score += 2
			# + 1 for non - children
			else:
				score += 1
		cycle_and_score[index] = score

	# Sort the key(index) by value(score) in descending order
	sortedCyclesByScore = sorted(cycle_and_score.items(), key = operator.itemgetter(1))
	sortedCyclesByScore.reverse()
	# print sortedCyclesByScore

	#greedily choose the cycles of highest score as the output, making sure all cycles are disjoint
	restricted_vertices = []
	solution = []

	for pair in sortedCyclesByScore:
		cycle = cycles[pair[0]]
		can_add = True
		for node in cycle:
			if node in restricted_vertices:
				can_add = False
				break;
		if can_add:
			solution.append(cycle)
			restricted_vertices.extend(cycle)

	for i in xrange(len(solution)):
		cycle = solution[i]
		solution[i] = cycleConstructor(cycle[1:], cycle[0], cycle[0])

	return solution

	# while cycle_and_score:
	# 	max_val_cycle_index = max(cycle_and_score.iteritems(), key=operator.itemgetter(1))[0]
	# 	max_val_cycle = cycles[max_val_cycle_index]
	# 	can_add = True
	# 	for node in max_val_cycle:
	# 		if node in restricted_vertices:
	# 			can_add = False
	# 			del cycle_and_score[max_val_cycle_index]
	# 			break
	# 	if can_add:
	# 		solution.append(max_val_cycle)
	# 		restricted_vertices.extend(max_val_cycle)
	# 		del cycle_and_score[max_val_cycle_index]

	# print "solution: ", solution
	# print len(solution)
	# return solution

def clear():
	global children
	global adjaMatrix
	global edges
	global cycles
	global numNodes
	children = []
	adjaMatrix = []
	edges = []
	cycles = []
	numNodes = 0
	G = None


def solveFlow(inputFileNumber):
	initializeAM(str(inputFileNumber))
	convertToEdges()
	simpleCycles()
	return solutionCycles()




def printSolution():
 
	ret = open("solution/leo.out", "w")
	#Converting solutionCycles --> valid output format
	for i in xrange(1, 493):
		flag = False

		# Get solution cycles
		currSol = solveFlow(i)
		print "instance: ", i
		print currSol
		clear()

		retStr = ""
		if currSol:
			#we return the cycles from the primary algorithm
			for cycle in currSol:
				if flag:
					retStr += " "
				else:
					flag = True
				for node in cycle:
					retStr += str(node)
					retStr += " "
				retStr = retStr[:-1]
				retStr += ";"
			#end of returning cycles 
			ret.write(retStr[:-1] + "\n")
		else:
			ret.write("None\n")

	ret.close()


# G = nx.DiGraph()
# G.add_edges_from([(1, 3), (3, 2), (2, 6), (6, 5), (5, 1), (2, 1), (1, 6), (6, 2)])
# print cycleConstructor([2, 6], 1, 1)
	
printSolution()

# print solveFlow(7)
# clear()
# for i in xrange(1, 2):
# 	initializeAM(str(i))
# 	convertToEdges()
# 	simpleCycles()
# 	print "instance ", i
# 	solution = solutionCycles()
# 	print solution
# 	for cycle in solution:
# 		   	for i in xrange(len(cycle)):
# 		   		row = int(cycle[i])
# 		   		col = int(cycle[(i + 1)%len(cycle)])
# 		   		if adjaMatrix[row][col] != 1:
# 		   			print "row: ", row, " col: ", col, "-->", adjaMatrix[row][col]
# 		   			print "error: instance " + str(i) + " has wrong cycle -> ", cycle
# 		   			break

	# clear()


# print ratio
# print min(ratio)
# print max(ratio)
# print "totally: ", count
# solveFlow("7")