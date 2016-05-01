#phase1-processed
import pprint, tarjan
fileName = "SAMPLEINSTANCE"


dct = {}

"""Function to return list of optimal, approximated cycles for a particular input file.
The input is a string e.g. '42' which is a repr of 42.in in the phase1-processed directory"""
def calcCycles(inputFileNumber):
	#Opening
	global dct

	f = open("phase1-processed/" + inputFileNumber + ".in", "r")
	numNodes = f.readline().split()
	numNodes = int(numNodes[0])
	print('numNodes ' + str(numNodes))	

	#Counting number of children
	readInChildren = f.readline().split()
	numChild = ''.join(readInChildren)
	childPenaltyUpperBound = 2 * len(numChild)
	if numChild in ['/n', '\r\n', ""]:
		numChild = []
	else:
		numChild = readInChildren

	#Total possible penalty = 2 * child vertices + 
	#Calculating total possible penality as a baseline comparison
	totalPenalty = childPenaltyUpperBound #TODO: add num of non-child nodes
	print "TOTAL POSSIBLE PENALTY", totalPenalty

	print(str(type(numChild)))
	print('numChild ', numChild)	


	dct = {}



	#Creating dictionary representation to pass into tarjan library
	for i in xrange(numNodes):
		line = f.readline().split()
		#checks each value is an int
		for j in xrange(numNodes):
			# print "line: ", 
			# print "line[j] is: ", line[j]
			if int(line[j]) == 1:
				# print("got inside the if statement")
				# if the node is already in the dictionary, extend its list of edges to include edge j
				if i in dct:
					print("about to modify index i: ", i)
					print("dict[i] was: ", dct[i])

					current_edges = dct[i]
					current_edges.append(j)
					print("dict[i] is now: ", dct[i])

				#if the node is not yet in the dictionary, add key i and value [j]
				else:
					print("about to create a new key, value for this index, ", i)
					dct[i] = [j]
					print("dict[i] is new: ", dct[i])

		print("dct is ", dct)

		listOfSCC = tarjan.tarjan(dct)
		print('\n Pretty List of SCCs \n')
		for scc in listOfSCC:
			if len(scc) < 2:
				listOfSCC.remove(scc)
			else:
				print(scc)

		
		print "\n Total cycles for ", fileName, ": ", listOfSCC
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


