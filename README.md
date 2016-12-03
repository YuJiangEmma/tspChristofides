# CS325-400 Group 31 Project 4 Readme
## Traveling Salesman Problem
Authors: Cas Donoghue, Patrick Kwong, and Nicholas Vrontakis

## Running the Program
1. Put the tsp.py program file in the same directory as your problem instance text file(s).
2. Run tsp.py on the command line with your problem instance file.

   ```
   python tsp.py tsp_example_1.txt
   ```
3. The program will write the results to a file named: [problem instance filename.txt].tour

## Input File Format
The input file has to be in the following format. Each line defines a city and each line has three numbers separated by white space.

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