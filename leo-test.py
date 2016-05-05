import pprint, tarjan
import networkx as nx

fileName = "SAMPLEINSTANCE"
# dct = {}
children = []
# listOfSCC = []
adjaMatrix = []
edges = []
cycles = []
numNodes = 0

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
		children = readInChildren

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


def simpleCycles():
	global cycles
	G = nx.DiGraph()
	G.add_edges_from(edges)

	nodes = []
	for i, j in edges:
		if i not in nodes:
			nodes.append(i)
	for i in nodes:
		for n in xrange(1, 5):
			cycles.extend([path + [i] for path in findPaths(G, i, n) if i in G.neighbors(path[-1])])

	# removeDuplicateCycles()
	return cycles


def removeDuplicateCycles():
	global cycles
	uniqueCycles = []
	def cycleCounted(cycle):
		for c in uniqueCycles:
			if len(cycle) == len(c):
				same = True
				for i in cycle:
					if i not in c:
						same = False
						break
				if same:
					return True
		return False			

	for cycle in cycles:
		if not cycleCounted(cycle):
			uniqueCycles.append(cycle)

	cycles = uniqueCycles



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

	
initializeAM("1")
convertToEdges()
# solutionCycles()
# print edges
print simpleCycles()
print len(cycles)
# print adjaMatrix
# print dct