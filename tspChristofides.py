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
nodesInGraph = helperFunctionsTSP.read_input_vals('tsp_example_1.txt')

#declare graph object with num nodes found in text file
completeGraph = KruskalsMST.Graph(len(nodesInGraph))
# added this hash table so that we only have to calculate distances betwee
# points one time. The key for the hash is a concatenated string of start node 
# to end node. example key from 3 to 4 is '34' (PLEASE CHECK LOGIG FOR COLLISIONS)
distDictionary = {}
# nodeNames = []   # list of node names. For use in mimMatch results
#make complete graph (i think this will do it?????)
for i in nodesInGraph:
    # nodeNames.append(i.name)
    for j in nodesInGraph:
        if i.name != j.name:
            distance = helperFunctionsTSP.dist(i,j)
            keyString = str(i.name) + str(j.name)
            distDictionary[keyString] = distance
            completeGraph.addEdge(i.name,j.name,distance)

## find min spanning tree by kruskal
mstONE = completeGraph.KruskalMST()

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

# HUNGARIAN 1 : input formatting
# build a matrix to do Kuhn-Munkres, The hungarian algorithm
# note that all distances are negated as to make the max pairing algo work (i think this is the only way to 
# do it in practice) also note that the idea here is to split the odd vertices (should always be even num 
# odd vertices in a complete graph) into a matrix 
# ex: if oddVertices = [0,1,3,4] 
# then   oddVertMatrix = _|3|4
#                        0|_|_|
#                        1|_|_|

# ########## hungarian 1
# oddVertMatrix = []
# splitFactor =  len(oddVertices)/2
# for i in range(splitFactor):
#     matrixRow = []
#     for j in range(splitFactor,(len(oddVertices))):
#         matrixRow.append(helperFunctionsTSP.lookupDist(oddVertices[i],oddVertices[j],distDictionary) * -1)
#         # matrixRow.append(str(oddVertices[i])+str(oddVertices[j]))
#     oddVertMatrix.append(matrixRow)


# ########## hungarian 2
# oddVertMatrix = []
# for i in range(len(oddVertices)):
#     matrixRow = []
#     for j in range(len(oddVertices)):
#         if i == j:
#             matrixRow.append(-1000000)
#         else:
#             matrixRow.append(helperFunctionsTSP.lookupDist(oddVertices[i],oddVertices[j],distDictionary) * -1)
#             # matrixRow.append(str(oddVertices[i])+str(oddVertices[j]))
#     oddVertMatrix.append(matrixRow)


# # BOTH HUNGARIAN !!!!! 
# # call the Kuhn-Munkres, The hungarian algorithm with matrix built for odd vertices
# oddMatches = minMatch.maxWeightMatching(oddVertMatrix)


# # NOTE: the hungarian algo returns 2 dictionaries and a useless number (|min matching sum|). The only thing we are interested in is the
# # first or second dictionary (they have the same info bc undirected graph...). The only trick will be that the values
# # returned ARE NOT THE NODE LABELS FOR THE MST, OR COMPLETE GRAPH!!!!!!! Instead they are simply the index to the 
# # oddVertices array. IF YOU WANT INFO ABOUT A NODE IN THE oddMatches result YOU MUST USE IT AS AN INDEX TO oddVertices!
# # just want to be explicit here because it is probably horrible design. Sorry. 

# Here we make an array of arrays (list of nodes) based on the hungarian result for strategy 1 hungarian

## HUNGARIAN 1 final pairings
# hungarianParings = []
# for key,val in oddMatches[0].items():
#     distanceTo = helperFunctionsTSP.lookupDist(oddVertices[key],oddVertices[val + splitFactor],distDictionary)
#     eachPair = [oddVertices[key],oddVertices[val + splitFactor],distanceTo]
#     hungarianParings.append(eachPair)
#     eachPair = [oddVertices[val + splitFactor],oddVertices[key],distanceTo]
#     hungarianParings.append(eachPair)



### HUngarian 2 SELECTION
#available nodes will be used for finding subset of perfect matchings
# avalableNodes = list(oddVertices)
# pairings = []
# #subset of half the total perfect matchings
# for k,v in oddMatches[0].items():
#     srtVtx = oddVertices[k]
#     endVtx = oddVertices[v]
#     if (srtVtx in avalableNodes) and (endVtx in avalableNodes):
#         pairings.append([srtVtx,endVtx])
#         avalableNodes.remove(srtVtx)
#         avalableNodes.remove(endVtx)

# ###HUNGARIAN 2 Final pairings
# hungarianParings = []
# for i in pairings:
#     distanceTo = helperFunctionsTSP.lookupDist(i[0],i[1],distDictionary)
#     eachPair = [i[0],i[1],distanceTo]
#     hungarianParings.append(eachPair)
#     eachPair = [i[1],i[0],distanceTo]
#     hungarianParings.append(eachPair)


##### SIMPLE GREEDY NO HUNGARIAN
# print "oddVertices"
# print oddVertices
nodesLeft = list(oddVertices)
hungarianParings = [] #note this name here is stupid, it needs to be changed, just making code later on work

while len(nodesLeft) > 0:
    valu = 100000000
    currNode = nodesLeft[0]
    for i in nodesLeft:
        if (currNode != i ) and (helperFunctionsTSP.lookupDist(currNode,i,distDictionary) < valu):
            valu = helperFunctionsTSP.lookupDist(currNode,i,distDictionary)
            closestMatch = i

    hungarianParings.append([currNode,closestMatch,valu])
    hungarianParings.append([closestMatch,currNode,valu])
    nodesLeft.remove(currNode)
    nodesLeft.remove(closestMatch)

# Simply re-format the MST data (SHOULD LOOK IN TO POSSIBLY DOING THIS ELSEWARE, DUPLICATING DATA kind of)
multiGraph = []
for i in mstONE:
    multiGraph.append(i)
    tempArray = [i[1],i[0],i[2]]
    multiGraph.append(tempArray)

# HOLY FUCKING SHIT THIS IS NOT UNION if statement is FUCKING ME
# this is a union of MST and the HUNGARIAN PAIRING graphs. 
# for i in hungarianParings:
#     if i not in multiGraph:
#         mstAdjacentcyList.addEdge(i[0],i[1],i[2])
#         tempArray = [i[0],i[1],i[2]]
#         multiGraph.append(tempArray)
#         tempArray = [i[1],i[0],i[2]]

# this is a union of MST and the HUNGARIAN PAIRING graphs. 
for i in hungarianParings:
    mstAdjacentcyList.addEdge(i[0],i[1],i[2])
    tempArray = [i[0],i[1],i[2]]
    multiGraph.append(tempArray)
    tempArray = [i[1],i[0],i[2]]

# At this point there should be a complete graph (one with an even number of odd degree nodes) 
# the fact that we have a complete graph makes a Euler tour possible. That is the next step. 

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
# print total
# #list the vertices in the TSP tour
# for i in hamCycle:
#     print i

##### TWO OPT NOT WORKING

# mostImproved = 0
# for i in range(len(hamCycle)):
#     length = len(hamCycle)
#     print i,(i+1)%length
#     print (i+2)%length,(i+3)%length

#     difference = (helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+1)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+3)%length],distDictionary)) - \
#     (helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+3)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+1)%length],distDictionary))

#     print hamCycle[i],hamCycle[(i+1)%length],hamCycle[(i+2)%length],hamCycle[(i+3)%length]
#     print helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+1)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+3)%length],distDictionary)

#     print (helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+3)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+1)%length],distDictionary))

#     if difference > mostImproved:
#         mostImproved = difference
#         print "swapped"
#         swap1 = (i+1)%length
#         swap2 = (i+3)%length
#         print swap1,swap2
#         print mostImproved

# if mostImproved > 0:
#     hamCycle[swap1],hamCycle[swap2] = hamCycle[swap2],hamCycle[swap1]
#     total -= mostImproved


# print hamCycle
# print total
# print helperFunctionsTSP.tspSolutionDist(hamCycle,distDictionary)
# print distDictionary

##### TWO OPT NOT WORKING

# print hamCycle
# print total
# for i in range(len(hamCycle)):
#     length = len(hamCycle)
#     # print i,(i+1)%length
#     # print (i+2)%length,(i+3)%length

#     difference = (helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+1)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+3)%length],distDictionary)) - \
#     (helperFunctionsTSP.lookupDist(hamCycle[i],hamCycle[(i+3)%length],distDictionary) + \
#     helperFunctionsTSP.lookupDist(hamCycle[(i+2)%length],hamCycle[(i+1)%length],distDictionary))

#     if difference > 0:
#         swap1 = (i+1)%length
#         swap2 = (i+3)%length
#         print difference
#         print hamCycle[i],swap1
#         print hamCycle[(i+2)%length],swap2
#         hamCycle[swap1],hamCycle[swap2] = hamCycle[swap2],hamCycle[swap1]
#         print hamCycle


# print hamCycle
# print helperFunctionsTSP.tspSolutionDist(hamCycle,distDictionary)
# print distDictionary

###### rudamentary 2OPT very slow

currentPath = hamCycle[:]


size = len(currentPath)
best_distance = helperFunctionsTSP.tspSolutionDist(currentPath,distDictionary)
improve = 0
while improve < 210:
    
    for i in range(size - 1):
        for j in range(i+1,size):
            testPath = currentPath[:]
            temp = []
            for x in range(i,j + 1):
                temp.append(testPath[x])
            for y in range(i,j + 1):
                testPath[y] = temp.pop()
            testDistance = helperFunctionsTSP.tspSolutionDist(testPath,distDictionary)
            if (testDistance < best_distance):
                currentPath = testPath[:]
                best_distance = testDistance
                #break
    improve += 1
  

print hamCycle
print total
print currentPath
print best_distance
