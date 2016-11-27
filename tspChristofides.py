#!/usr/bin/python
# Python program for Kruskal's algorithm to find Minimum Spanning Tree
# of a given connected, undirected and weighted graph
 
from collections import defaultdict
# import math, re, sys
import adjacentcy
import minMatch
import KruskalsMST
import helperFunctionsTSP
import hierholzer

##### TEST DRIVER#################

# read in the data (will return with a list of Vertex)
nodesInGraph = helperFunctionsTSP.read_input_vals('mstTest.txt')

#declare graph object with num nodes found in text file
completeGraph = KruskalsMST.Graph(len(nodesInGraph))
# added this hash table so that we only have to calculate distances betwee
# points one time. The key for the hash is a concatenated string of start node 
# to end node. example key from 3 to 4 is '34' (PLEASE CHECK LOGIG FOR COLLISIONS)
distDictionary = {}
#make complete graph (i think this will do it?????)
for i in nodesInGraph:
    for j in nodesInGraph:
        if i.name != j.name:
            distance = helperFunctionsTSP.dist(i,j)
            keyString = str(i.name) + str(j.name)
            distDictionary[keyString] = distance
            completeGraph.addEdge(i.name,j.name,distance)

## find min spanning tree by kruskal
mstONE = completeGraph.KruskalMST()
#multiGraph is for storing union of MST and min weight matching of odd degree vertices
multiGraph = []
## convert mstONE to adjacentcy list representation
mstAdjacentcyList = adjacentcy.adjacentcyGraph()
for i in range(len(mstONE) + 1):
    mstAdjacentcyList.addVertex(i)
## since graph is not directed connect everything "twice"
for i in mstONE:
    mstAdjacentcyList.addEdge(i[0],i[1],i[2])
    mstAdjacentcyList.addEdge(i[1],i[0],i[2])

# find odd vertices in MST 
oddVertices = []
for v in mstAdjacentcyList:
    if v.degree % 2 != 0:
        oddVertices.append(v.id)

# build a matrix to do Kuhn-Munkres, The hungarian algorithm
# note that all distances are negated as to make the max pairing algo work (i think this is the only way to 
# do it in practice) also note that the idea here is to split the odd vertices (should always be even num 
# odd vertices in a complete graph) into a matrix 
# ex: if oddVertices = [0,1,3,4] 
# then   oddVertMatrix = _|3|4
#                        0|_|_|
#                        1|_|_|
oddVertMatrix = []
splitFactor =  len(oddVertices)/2
for i in range(splitFactor):
    matrixRow = []
    for j in range(splitFactor,(len(oddVertices))):
        matrixRow.append(helperFunctionsTSP.lookupDist(oddVertices[i],oddVertices[j],distDictionary) * -1)
        # matrixRow.append(str(oddVertices[i])+str(oddVertices[j]))
    oddVertMatrix.append(matrixRow)


# call the Kuhn-Munkres, The hungarian algorithm with matrix built for odd vertices
oddMatches = minMatch.maxWeightMatching(oddVertMatrix)
# NOTE: the hungarian algo returns 2 dictionaries and a useless number (|min matching sum|). The only thing we are interested in is the
# first or second dictionary (they have the same info bc undirected graph...). The only trick will be that the values
# returned ARE NOT THE NODE LABELS FOR THE MST, OR COMPLETE GRAPH!!!!!!! Instead they are simply the index to the 
# oddVertices array. IF YOU WANT INFO ABOUT A NODE IN THE oddMatches result YOU MUST USE IT AS AN INDEX TO oddVertices!
# just want to be explicit here because it is probably horrible design. Sorry. 

# Here we make an array of arrays (list of nodes) based on the hungarian result
hungarianParings = []
for key,val in oddMatches[0].items():
    distanceTo = helperFunctionsTSP.lookupDist(oddVertices[key],oddVertices[val + splitFactor],distDictionary)
    eachPair = [oddVertices[key],oddVertices[val + splitFactor],distanceTo]
    hungarianParings.append(eachPair)
    eachPair = [oddVertices[val + splitFactor],oddVertices[key],distanceTo]
    hungarianParings.append(eachPair)


# Simply re-format the MST data (SHOULD LOOK IN TO POSSIBLY DOING THIS ELSEWARE, DUPLICATING DATA kind of)
multiGraph = []
for i in mstONE:
    multiGraph.append(i)
    tempArray = [i[1],i[0],i[2]]
    multiGraph.append(tempArray)

# this is a union of MST and the HUNGARIAN PAIRING graphs. 
for i in hungarianParings:
    if i not in multiGraph:
        mstAdjacentcyList.addEdge(i[0],i[1],i[2])
        tempArray = [i[0],i[1],i[2]]
        multiGraph.append(tempArray)
        tempArray = [i[1],i[0],i[2]]


# At this point there should be a complete graph (one with an even number of odd degree nodes) 
# the fact that we have a complete graph makes a Euler tour possible. That is the next step. 

# the hierholzer algo is being fucking up right now works on mstTest.txt but not on tsp_example_X.txt
# format input by adding all edges (directed)
hierholzerNodes = []
hierholzerEdges = []

for i in nodesInGraph:
    hierholzerNodes.append(i.name)
for i in multiGraph:
    edgeL = [i[0],i[1]]
    hierholzerEdges.append(edgeL)

# call hierholzer with formatted input
eulerTour = hierholzer.hierholzer(hierholzerNodes,hierholzerEdges)
# make ham cycle w/shortcuts
hamCycle = []
for i in eulerTour:
    if i not in hamCycle:
        hamCycle.append(i)

# call total helper function (will just sum the path)
total = helperFunctionsTSP.tspSolutionDist(hamCycle,distDictionary)
print total
#list the vertices in the TSP tour
for i in hamCycle:
    print i

