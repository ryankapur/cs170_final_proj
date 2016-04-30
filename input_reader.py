#phase1-processed
import pprint, tarjan

f = open("phase1-processed/94.in", "r")
numNodes = f.readline().split()
numNodes = int(numNodes[0])
print('numNodes ' + str(numNodes))	

children = []


numChildren = f.readline().split()
numChild = ''.join(numChildren)
if numChild in ['/n', '\r\n', ""]:
	numChild = []
else:
	numChild = numChildren

print(str(type(numChild)))
print('numChild ', numChild)	


# for line in f:
# 	print('for lines', str(line))


#create 2D array logic
d = [[0 for j in range(numNodes)] for i in range(numNodes)]

dct = {}



#Creating dictionary representation to pass into tarjan library
for i in xrange(numNodes):
	line = f.readline().split()
	#checks each value is an int
	for j in xrange(numNodes):
		print "line: ", 
		print "line[j] is: ", line[j]
		if int(line[j]) == 1:
			print("got inside the if statement")
			#if the node is already in the dictionary, extend its list of edges to include edge j
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




for i in range(0, len(d)):
	for j in range(0,len(d[0])):
		print "d at: ", i, " ", j, " ", d[i][j]

print("dct is ", dct)

result = tarjan.tarjan(dct)
for scc in result:
	if len(scc) < 2:
		result.remove(scc)

print 'result jajaja ', result


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


