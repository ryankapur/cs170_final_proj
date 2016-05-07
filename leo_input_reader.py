
import pprint, tarjan
import networkx as nx
from collections import defaultdict
import operator

fileName = "SAMPLEINSTANCE"
dct = {}
children = []
listOfSCC = []
adjaMatrix = []
numNodes = 0

"""Function to return list of optimal, approximated cycles for a particular input file.
The input is a string e.g. '42' which is a repr of 42.in in the phase1-processed directory"""
def calcCycles(inputFileNumber):
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

	dct = {}
	adjaMatrix = []
	#Creating dictionary representation to pass into tarjan library
	for i in xrange(numNodes):
		line = f.readline().split()
		adjaMatrix.append(line)

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
		
	# #remove all SCCs of length 1 or less
	# for scc in listOfSCC:
	# 	if len(scc) < 2:
	# 		listOfSCC.remove(scc)

		
	# print "\n SCCS for file: ", fileName, ": ", listOfSCC
		# print "dictionary : ", dct


#Do calculations for each file in dir
#TODO: map the cycles ouputted to each file to a newline in finaloutput.out
# calcCycles(fileName)

def densityOfGraph():
	count = 0.0
	for row in xrange(numNodes):
		for col in xrange(numNodes):
			if adjaMatrix[row][col] == "1":
				count += 1
 	return count / numNodes**2



""""Take dct initialized by calcCycles() and
	turn it into edges representation of the 
	graph. Write edges into edges.txt file as
	an input file of Johnson's algorithm."""
def dctToEdges():
	inputString = ""
	for row in xrange(numNodes):
		for col in xrange(numNodes):
			if adjaMatrix[row][col] == "1":
				inputString = inputString + str(row) + " " + str(col) + "\n"

	# for key in dct:
	# 	for value in dct[key]:
	# 		inputString = inputString + str(key) + " " + str(value) + "\n"
			# print str(key) + " " + str(value) + "\n"
	# print inputString

	f = open("edges.txt", "w")
	f.write(inputString)
	f.close()

# dctToEdges()





def simple_cycles(G):
    def _unblock(thisnode):
        """Recursively unblock and remove nodes from B[thisnode]."""
        if blocked[thisnode]:
            blocked[thisnode] = False
            while B[thisnode]:
                _unblock(B[thisnode].pop())

    def circuit(thisnode, startnode, component):
        closed = False # set to True if elementary path is closed
        path.append(thisnode)
        blocked[thisnode] = True
        for nextnode in sorted(component[thisnode]): # direct successors of thisnode
            if nextnode == startnode:
                result.append(path + [startnode])
                closed = True
            elif not blocked[nextnode]:
                if circuit(nextnode, startnode, component):
                    closed = True
        if closed:
            _unblock(thisnode)
        else:
            for nextnode in component[thisnode]:
                if thisnode not in B[nextnode]: # TODO: use set for speedup?
                    B[nextnode].append(thisnode)
        path.pop() # remove thisnode from path
        return closed

    path = [] # stack of nodes in current path
    blocked = defaultdict(bool) # vertex: blocked from search?
    B = defaultdict(list) # graph portions that yield no elementary circuit
    result = [] # list to accumulate the circuits found
    # Johnson's algorithm requires some ordering of the nodes.
    # They might not be sortable so we assign an arbitrary ordering.
    ordering=dict(zip(sorted(G),range(len(G))))
    for s in sorted(ordering.keys()):
        # Build the subgraph induced by s and following nodes in the ordering
        subgraph = G.subgraph(node for node in G 
                              if ordering[node] >= ordering[s])
        # Find the strongly connected component in the subgraph 
        # that contains the least node according to the ordering
        strongcomp = nx.strongly_connected_components(subgraph)
        mincomp=min(strongcomp, 
                    key=lambda nodes: min(ordering[n] for n in nodes))
        component = G.subgraph(mincomp)
        if component:
            # smallest node in the component according to the ordering
            startnode = min(component,key=ordering.__getitem__) 
            for node in component:
                blocked[node] = False
                B[node][:] = []
            dummy=circuit(startnode, startnode, component)

    return result


# G = nx.DiGraph()



# # for edge in sys.stdin.readlines():
# inputf = open("edges.txt", "r")
# for edge in inputf.readlines():
#     v1,v2 = edge.split(' ', 1)
#     G.add_edge(v1.strip(),v2.strip())


# # print simple_cycles(G)
# outputf = open("possibleCycles.txt", "w")
# for c in simple_cycles(G):
#     if len(c) <= 6 :
#         outputf.write(" ".join(c[:-1]) + "\n\n")
# outputf.close()
#Run Johnson's Algorithm within input_reader
#for now, will return a list of the optimal cycles given by the greedy algorithm
def solutionCycles():
	G = nx.DiGraph()


	# create G
	inputf = open("edges.txt", "r")
	for edge in inputf.readlines():
	    v1,v2 = edge.split(' ', 1)
	    G.add_edge(v1.strip(),v2.strip())

	# print "Let's start"

	#put all possible cycles of length 5 or smaller in a list
	simple_sol = []
	for c in simple_cycles(G):
	    if len(c) <= 6 :
	    	# print c
	    	simple_sol.append(c[:-1])

	# print "I've finished simple cycles detection!"

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


	# print "simple solution not considering disjoint cycles was ", simple_sol
	# print "after greedily choosing disjoint cycles, solution is ", solution
	print solution

# solutionCycles()


# for i in range(262, 263):
# 	print "case", i
# 	calcCycles(str(i))
# 	# maxLen = 0
# 	# for ls in listOfSCC:
# 	# 	if len(ls) > maxLen:
# 	# 		maxLen = len(ls)
# 	# if maxLen > 100:
# 	# 	continue;
# 	dctToEdges()
# 	solutionCycles()


f = open("density.txt", "w")
count = 0
for i in xrange(1, 493):
	calcCycles(str(i))
	density = densityOfGraph()
	maxSizeOfSCC = 0
	for ls in listOfSCC:
		if len(ls) > maxSizeOfSCC:
			maxSizeOfSCC = len(ls)
	# if density*numNodes*numNodes < 210:
	# 	print "instance", i
	# 	dctToEdges()
	# 	solutionCycles()
	# 	count += 1
	s = "instance " + str(i) + "\tdensity: " + "%.5f"%density + "\tnumEdges: " + str(int(density*numNodes*numNodes)) + "\n"
	print s
	f.write(s)
# f.write("numEdges < 210 : " + str(count))
# f.close()


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


