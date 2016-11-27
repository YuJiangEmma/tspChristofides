#!/usr/bin/python
# These are just some functions i've made for some random stuff
# simple class for doing file in and building graph

import math, re, sys

class vertex:
    def __init__(self,name,xcoord,ycoord):
        self.name = name
        self.xcoord = xcoord
        self.ycoord = ycoord

#distance function for euclidean distance from csu
def dist(xy1, xy2):
    
    return int(round(math.sqrt((xy1.xcoord - xy2.xcoord)**2 + (xy1.ycoord - xy2.ycoord)**2)))
#modified from provided files. i like the way they parse the input file w/RE
def read_input_vals(in_file):
    # each line of in_file shoudl have a label as its first int on each line,
    # this captures a list of those labels
    # (expected from 0 to n - 1, but only uniqueness is necessary)
    
    file = open(in_file,'r')
    line = file.readline()
    
    #points tracks the points as teh key and the number of visitations as the value at that key
    points = []
    while len(line) > 1:
        line_parse = re.findall(r'[^,;\s]+', line)
        newNode = vertex(int(line_parse[0]),int(line_parse[1]),int(line_parse[2]))
        points.append(newNode)
        line = file.readline()
    file.close()
    
    return points

def lookupDist(origin,destination,dictionary):
    lookup = str(origin) + str(destination)
    return dictionary[lookup]

def tspSolutionDist(hamCycle,distDictionary):
    total = 0
    for i in range(len(hamCycle) - 1):
        total += lookupDist(hamCycle[i],hamCycle[(i+1)],distDictionary)
    total += lookupDist(hamCycle[-1],hamCycle[(0)],distDictionary)
    return total