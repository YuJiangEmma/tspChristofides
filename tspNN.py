#!/usr/local/bin/python
#
# CS325 Project 4: Traveling Salesman Solution 
# Nearest Neighbor Algorithm
#
# Group 31
# Cas Donoghue
# Patrick Kwong
# Nicholas Vrontakis

import sys
import math
import time
import itertools
import exceptions

start = time.clock()
input_file = sys.argv[1]

#############
# functions #
#############
# source: used code from provide project 4 files and nearest neighbor algorithm from https://github.com/dozer/TravelingSalesmanProblem/blob/master/tsp_greedy/src/NN_tsp.py

# Euclidean distance rounded to the nearest integer
def get_distance(a,b):
	dx = a[1]-b[1]
	dy = a[2]-b[2]
	return int(round(math.sqrt(dx*dx + dy*dy)))


# get cities from file
def get_cities(filename):
	for line in filename:
		try:
			parts = line.split()
			if parts[0].isdigit():
				# parse city to [ident, x-coor, y-coor, visited(t/f)]
				city = [int(parts[0]), int(parts[1]), int(parts[2].strip('\n')), False]
				cities.append(city)
		except Exception as e:
			pass


# calculate the nearest neighbor of city
def get_nearest_neighbor(i):
	nearest = [0, float("inf")]
	for index in range(len(cities)):
		# skip if looking at current city or a city that has been visited
		if i == index or cities[index][3] == True:
			pass
		# calculate distance
		else:
			distance = get_distance(cities[i], cities[index])
			if distance < nearest[1]:
				nearest = [index, distance]
	# set the city to visited
	cities[nearest[0]][3] = True
	return nearest


# nearest neighbor algorithm
def nearest_neighbor(cities):
	data = []
	tour = [[], 0]
	first = get_nearest_neighbor(0)
	data.append(first)
	next = first

	# get the nearest neighbor and weight for every vertex
	for index in range(1, len(cities)):
		current = get_nearest_neighbor(next[0])
		data.append(current)
		next = current

	for element in data:
		tour[1] += element[1]
		tour[0].append(element[0])

	# remove duplicated weight of first city to second city
	tour[1] -= get_distance(cities[tour[0][0]], cities[tour[0][1]])
	# include weight of last city to first city
	tour[1] += get_distance(cities[tour[0][-1]], cities[tour[0][0]])

	return tour


# output filename
def output_filename(filename):
	filename = filename.split(".")
	out_file = filename[0] + ".txt.tour"
	return out_file


# write tour length and tour sequence to input_filename.txt.tour
def write_output_file(tour):
	with open(output_filename(input_file), "w" ) as out:
		out.write(str(tour[1]))
		out.write("\n")

		for i in range(len(tour[0])):
			out.write(str(tour[0][i]))
			out.write("\n")


###############
# Main Script #
###############

cities = []
cities_file = open(input_file)
get_cities(cities_file)

start = time.time()
best_tour = nearest_neighbor(cities)
finish = time.time()

print 'Best tour found: %s' % (best_tour[0])
print 'Best tour found length: %d' % (best_tour[1])
print 'Number of cities: %d' % (len(best_tour[0]))
print 'Time to calculate: %0.3f seconds' % (finish - start)

write_output_file(best_tour)