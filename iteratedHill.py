# hill climbing search with random restarts of the ackley objective function
import time
import numpy as np
from numpy import asarray
from numpy import arange
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed
from numpy import meshgrid
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

def objectiveforplot(x, y):
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20


# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20

# check if a point is within the bounds of the search
def in_bounds(point, bounds):
	# enumerate all dimensions of the point
	for d in range(len(bounds)):
		# check if out of bounds for this dimension
		if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
			return False
	return True

# hill climbing local search algorithm
def hillclimbing(objective, bounds, n_iterations, step_size, start_pt):
	# store the initial point
	solution = start_pt
	result1 = []
	# evaluate the initial point
	solution_eval = objective(solution)
	x, y = solution
	temp_Arr = [x,y,solution_eval]
	result1.append(temp_Arr)        
	# run the hill climb
	for i in range(n_iterations):
		# take a step
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds):
			candidate = solution + randn(len(bounds)) * step_size
		# evaluate candidate point
		candidte_eval = objective(candidate)
		# check if we should keep the new point
		if candidte_eval <= solution_eval:
			# store the new point
			solution, solution_eval = candidate, candidte_eval
			x, y = solution
			temp_Arr = [x,y,solution_eval]
			result1.append(temp_Arr)
	result.append(result1)
	return [solution, solution_eval]

# hill climbing with random restarts algorithm
def random_restarts(objective, bounds, n_iter, step_size, n_restarts):
	best, best_eval = None, 1e+10
	# enumerate restarts
	for n in range(n_restarts):
		# generate a random initial point for the search
		start_pt = None
		while start_pt is None or not in_bounds(start_pt, bounds):
			start_pt = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		# perform a stochastic hill climbing search
		solution, solution_eval = hillclimbing(objective, bounds, n_iter, step_size, start_pt)
		# check for new best
		if solution_eval < best_eval:
			best, best_eval = solution, solution_eval
			print('Restart %d, best: f(%s) = %.5f' % (n, best, best_eval))
		else:
			del result[-1]	
	return [best, best_eval]

# seed the pseudorandom number generator
seed(1)
# define range for input
bounds = asarray([[-5.0, 5.0], [-5.0, 5.0]])
# define the total iterations
n_iter = 1000
# define the maximum step size
step_size = 0.05
# total number of random restarts
n_restarts = 200
# perform the hill climbing search

#result
result = []

best, score = random_restarts(objective, bounds, n_iter, step_size, n_restarts)
print('Done!')
print('f(%s) = %f' % (best, score))

np_result =  np.array(result, dtype=object)

#Plotting
# define range for input
r_min, r_max = -5.0, 5.0
# sample input range uniformly at 0.1 increments
xaxis = arange(r_min, r_max, 0.05)
yaxis = arange(r_min, r_max, 0.05)
# create a mesh from the axis
x, y = meshgrid(xaxis, yaxis)
# compute targets
results = objectiveforplot(x, y)
# create a surface plot with the jet color scheme
figure = pyplot.figure()
axis = figure.gca(projection='3d')

for i in range(3):
    axis.plot3D(np_result[i][:][0], np_result[i][:][1], np_result[i][:][2], 'Orange')
    axis.scatter3D(np_result[i][:][0], np_result[i][:][1], np_result[i][:][2], c = np_result[i][:][2], cmap='hsv')

axis.plot3D(np_result[3][:][0], np_result[3][:][1], np_result[3][:][2], 'blue')
axis.scatter3D(np_result[3][:][0], np_result[3][:][1], np_result[3][:][2], c = np_result[3][:][2], cmap='pink')
pyplot.show()