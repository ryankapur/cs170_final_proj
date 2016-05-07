





fileName = "SAMPLEINSTANCE"
# dct = {}
children = []
# listOfSCC = []
adjaMatrix = []
numNodes = 0

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
		line = f.readline().split()
		adjaMatrix.append(line)

		# for j in xrange(numNodes):
		# 	if int(line[j]) == 1:
		# 		# if the node is already in the dictionary, extend its list of edges to include edge j
		# 		if i in dct:
		# 			current_edges = dct[i]
		# 			current_edges.append(j)
		# 		#if the node is not yet in the dictionary, add key i and value [j]
		# 		else:
		# 			dct[i] = [j]


	# listOfSCC = tarjan.tarjan(dct)


def chechCycle(inputFileNumber):
	initializeAM(inputFileNumber)
	inputf = open("solution/solutions.out", "r")
	line = inputf.readlines()[int(inputFileNumber) - 1].split(";")
	if line[0] != "None\n":
		for cycle in line:
			cycle = cycle.split()
			# print cycle
		   	for i in xrange(len(cycle)):
		   		row = int(cycle[i])
		   		col = int(cycle[(i + 1)%len(cycle)])
		   		if adjaMatrix[row][col] != "1":
		   			print "row: ", row, " col: ", col, "-->", adjaMatrix[row][col]
		   			print "error: instance " + inputFileNumber + " has wrong cycle -> ", cycle
		   			if inputFileNumber not in instanceList:
		   				instanceList.append(inputFileNumber)
		   			break

def clear():
	global adjaMatrix
	global children
	global numNodes

	adjaMatrix = []
	children = []
	numNodes = 0


instanceList = []

for i in xrange(1, 493):
	chechCycle(str(i))
	clear()

print instanceList
