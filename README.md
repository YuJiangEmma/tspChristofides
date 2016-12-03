# CS325-400 Group 31 Project 4 Readme
## Traveling Salesman Problem (TSP)
Authors: Cas Donoghue, Patrick Kwong, and Nicholas Vrontakis

## Running the TSP Program
1. Put the the following files in the same directory as your problem instance text file(s). See section below for problem instance text file format.
⋅⋅* helperFunctionsTSP.py
⋅⋅* hierholzer.py
⋅⋅* newKruskal.py
⋅⋅* TSPcomp.py

2. Run the program file, TSPcomp.py on the command line with your problem instance file.

   ```
   python TSPcomp.py tsp_example_1.txt
   ```
3. The program will write the results to a file named: [problem instance filename.txt].tour

## Problem Instance Text File Format
The problem instance text file has to be in the following format. Each line defines a city and each line has three numbers separated by white space.

1. The first number is the city identifier.
2. The second number is the city’s x-coordinate.
3. The third number is the city’s y-coordinate.

   ```
    0 200 800
	1 3600 2300
	2 3100 3300
	3 4700 5750
	4 5400 5750
	5 5608 7103
	...
   ```