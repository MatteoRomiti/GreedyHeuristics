#GREEDY HEURISTIC ALGORITHM

from __future__ import division
from random import randint
from random import shuffle

#set this value to 1 for the random algo
rand_algo = 1

#set this value to 1 for a verbose run
prnt = 0

def make_route(i,d,path=[],visited=[]):
	global path_found
	visited.append(i)
	if link_matrix[i][d]==1:
		path.append([i,d])
		visited.append([d])	
		path_found += 1
		return path
	else:	
		for j in range(n_nodes):			
			if (j!=i and not(j in visited)):				
				if link_matrix[i][j]==1:
					path.append([i,j])
					visited.append([j])
					if j==d:
						return path
						path_found += 1
					else:
						return make_route(j,d,path,visited)

n_nodes = 10
delta = 6
path_found = 0

requested_number_of_positive_simulations = 10
#additional paths to find for the remaining traffic
total_paths = 0
positive_simulations = []

while(len(positive_simulations)<requested_number_of_positive_simulations):
	#repeat the experiment
	path_found = 0
	total_paths = 0

	# all-zeros traffic matrix
	t_matrix_low = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
	t_matrix_high = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
	#final traffic matrix
	t_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
	flow_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]

	# uniform matrix of low traffic flow that must go from s to d
	for i in range(n_nodes):
		for j in range(n_nodes):
			if j != i:
				t_matrix_low[i][j] = randint(5, 15)/10
	
	# uniform matrix of high traffic flow that must go from s to d
	for i in range(n_nodes):
		for j in range(n_nodes):
			if j != i:
				t_matrix_high[i][j] = randint(5, 15)

	if(prnt):
		print"t_matrix_low:"
		for i in range(n_nodes):	
			print t_matrix_low[i]
		print"t_matrix_high:"
		for i in range(n_nodes):	
			print t_matrix_high[i]

	#create the final traffic matrix
	for i in range(n_nodes):
		for j in range(n_nodes):
			if j != i:
				#probability = 0.1
				x = randint(1,10)
				if (x==1):
					t_matrix[i][j] = t_matrix_high[i][j]
				else:
					t_matrix[i][j] = t_matrix_low[i][j]

	# flows vector
	f_vector = []
	rand_f_vector = []
	for i in range(n_nodes):
		for j in range(n_nodes):
			f_vector.append([t_matrix[i][j], i, j]) # [traffic flow of the link][i][j]
			rand_f_vector.append([t_matrix[i][j], i, j]) # [traffic flow of the link][i][j]

	if (not(rand_algo)):
		f_vector.sort(reverse=True)
		if(prnt):	
			print "f_vector"
			for i in range(len(f_vector)):	
				print f_vector[i]

	else:
		shuffle(rand_f_vector)
		if(prnt):
			print "rand_f_vector"
			for i in range(len(rand_f_vector)):	
				print rand_f_vector[i]

	# 1 if link is present, 0 otherwise
	link_matrix= [[0 for x in range(n_nodes)] for j in range(n_nodes)]

	sum_lightpaths_in = [0 for x in range(n_nodes)]
	sum_lightpaths_out = [0 for x in range(n_nodes)]

	# check all flows to send
	for i in range(len(f_vector)):

		# reset these values to zero 
		sum_lightpaths_in = [0 for x in range(n_nodes)]
		sum_lightpaths_out = [0 for x in range(n_nodes)]
		
		# update the sum of lightpaths in and out from node x
		for x in range(n_nodes):
			for y in range(n_nodes):
				sum_lightpaths_in[x] += link_matrix[y][x]
				sum_lightpaths_out[x] += link_matrix[x][y]

		if(not(rand_algo)):
			if f_vector[i][0] != 0:
					# check all the lightpaths in and out of node i and node j 
				if sum_lightpaths_out[f_vector[i][1]] < delta and sum_lightpaths_in[f_vector[i][2]] < delta:
					# create the link
					link_matrix[f_vector[i][1]][f_vector[i][2]] = 1
		else:
			if rand_f_vector[i][0] != 0:
				# check all the lightpaths in and out of node i and node j 
				if sum_lightpaths_out[rand_f_vector[i][1]] < delta and sum_lightpaths_in[rand_f_vector[i][2]] < delta:
					# create the link
					link_matrix[rand_f_vector[i][1]][rand_f_vector[i][2]] = 1

	if(prnt):
		print "\nlink_matrix:"
		for i in range(n_nodes):
			print link_matrix[i]
		print "\nsum_lightpaths_out:"
		print sum_lightpaths_out
		print "\nsum_lightpaths_in:"
		print sum_lightpaths_in

	for i in range(n_nodes):
		for j in range(n_nodes):
			flow_matrix[i][j]=t_matrix[i][j]*link_matrix[i][j]

	# traffic sent in one hop
	if(prnt):
		print"\nflow_matrix:"
		for i in range(n_nodes):	
			print flow_matrix[i]

	# routes to re-enroute
	for s in range(n_nodes):
		for d in range(n_nodes):
			if s!=d and link_matrix[s][d]==0:
				# flow to send
				flujo = t_matrix[s][d]
				path=[]
				total_paths += 1
				make_route(s,d,path,[])				
				for x in range(len(path)):   
					#update the new flows
					flow_matrix[  path[x][0] ][ path[x][1]  ]+=t_matrix[s][d]
	if(prnt):
		print"\nflow_matrix:"
		for i in range(n_nodes):	
			print flow_matrix[i]

	f_vector_constraints = []
	for i in range(n_nodes):
		for j in range(n_nodes):
			f_vector_constraints.append([flow_matrix[i][j], i, j]) # [traffic flow of the link][i][j]

	f_vector_constraints.sort(reverse=True)

	if(path_found==total_paths):
		positive_simulations.append(f_vector_constraints[0][0])
		average = sum(positive_simulations)/len(positive_simulations)
		print str(average)
