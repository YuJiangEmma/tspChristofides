#!/usr/bin/python
# adapted data structure from http://interactivepython.org/runestone/static/pythonds/Graphs/Implementation.html
# purpose is adjacenty list for MST, Odd degree vertices, perfect matching and euler tour. 
# basically, space efficent data structure for TSP route (a sparse graph) 

class adjacentcyNode:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.degree = 0 #i added this attribute to keep track of degree for use in doing min matching analysis

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
        self.degree += 1

    def removeNeighbor(self,nbr):
        if nbr in self.connectedTo:
            del self.connectedTo[nbr]
        self.degree -= 1

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]



class adjacentcyGraph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = adjacentcyNode(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def removeEdge(self,f,t):
        self.vertList[f].removeNeighbor(self.vertList[t])

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
