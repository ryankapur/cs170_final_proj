#phase1-processed
import pprint

f = open("phase1-processed/95.in", "r")
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
for i in xrange(numNodes):
	line = f.readline().split()
	
	#checks each value is an int
	for j in xrange(numNodes):
		if not line[j].isdigit():
			print "Line " + str(i+2) + " must contain numNodes integers."
		d[i][j] = int(line[j])
		# if d[i][j] < 0 or d[i][j] > 1:
		# 	return "The adjacency matrix must be comprised of 0s and 1s."

# for i in xrange(numNodes):
# 	if d[i][i] != 0:
# 		return "A node cannot have an edge to itself."

for i in range(0, len(d)):
	for j in range(0,len(d[0])):
		print "d at: ", i, " ", j, " ", d[i][j]
