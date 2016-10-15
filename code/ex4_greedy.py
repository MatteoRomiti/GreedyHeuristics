from __future__ import division
from random import randint
from math import sqrt
from operator import itemgetter

# return the indeces of the place in the manh with the highest available number of 
# neighbors and the indeces of these neighbors 
def get_best_place(manh_size):
	# if we are here, there is at least one free place in the manh
	target = 4
	flag = 0
	while target>=0:
		# look at each place of the manh
		for i in range(manh_size):
			for j in range(manh_size):
				free_neighbors = []
				# check if this place is free
				if manh[i][j]==empty:
					flag = 1
					# check all the neighbors
					# right
					if manh[i][(j+1)%manh_size]==empty:
						free_neighbors.append([i,(j+1)%manh_size])
					# left
					if manh[i][(j+manh_size-1)%manh_size]==empty:
						free_neighbors.append([i,(j+manh_size-1)%manh_size])
					# down
					if manh[(i+1)%manh_size][j]==empty:
						free_neighbors.append([(i+1)%manh_size,j])
					# up
					if manh[(i+manh_size-1)%manh_size][j]==empty:
						free_neighbors.append([(i+manh_size-1)%manh_size,j])
					if target==len(free_neighbors):
						return i, j, free_neighbors
					if i==(manh_size-1) and j==(manh_size-1):
						# we checked all the free places and the target was too high, decrease it
						target -= 1

def check_and_send(keys, flow):
	for k in range(len(keys)):
		if keys[k] in flows:
			flows[keys[k]] += flow
		else:
			flows[keys[k]] = flow
	return

def check_row(s2,d1,d2,keys,flow):
	# check if this is the neighbor
	if s2==d2:
		check_and_send(keys, flow)
	# check if it is a right neighbor
	if (s2+1)%manh_size==d2:
		keys.append(str(d1) + str(s2) + str(d1) + str(d2))
		check_and_send(keys, flow)
	# check if it is a right-right neighbor
	if (s2+2)%manh_size==d2:
		# right
		keys.append(str(d1) + str(s2) + str(d1) +str((s2+1)%manh_size))
		# right
		keys.append(str(d1) +str((s2+1)%manh_size) + str(d1) +str(d2))
		check_and_send(keys, flow)
	# check if it is a left neighbor
	if (s2+manh_size-1)%manh_size==d2:
		keys.append(str(d1) + str(s2) + str(d1) +str(d2))
		check_and_send(keys, flow)
	return

n_nodes = 16
requested_n_of_simulations = 10000
simulations = []

while(len(simulations)<requested_n_of_simulations):
	# create a random traffic matrix
	t_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
	for i in range(n_nodes):
		for j in range(n_nodes):
			if j != i:
				t_matrix[i][j] = randint(5, 15)/10

	# join the traffic i-j with traffic j-i (half matrix under the diagonal will be zero)
	joined_t_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
	for i in range(n_nodes):
		for j in range(i):
			joined_t_matrix[j][i] = t_matrix[i][j] + t_matrix[j][i]

	f_vector = []
	for i in range(n_nodes):
		for j in range(n_nodes):
			if t_matrix[i][j] != 0:
				f_vector.append([t_matrix[i][j], i, j])

	joined_f_vector = []
	for i in range(n_nodes):
		for j in range(n_nodes):
			if joined_t_matrix[i][j] != 0:
				joined_f_vector.append([joined_t_matrix[i][j], i, j])

	joined_f_vector.sort(reverse=True)

	# find the node which exchange more traffic
	# total_nodes_traffic[i][0] is the total traffic of node total_nodes_traffic[i][1]   
	total_nodes_traffic = [] 

	for n in range(n_nodes):
		sum_node_traffic = 0 # sum of the total traffic of node n
		# sum all the traffic from node n
		for i in range(len(joined_f_vector)):
			if (joined_f_vector[i][1]==n or joined_f_vector[i][2]==n):
				sum_node_traffic += joined_f_vector[i][0]
		total_nodes_traffic.append([sum_node_traffic, n])

	total_nodes_traffic.sort(reverse=True)

	manh_size = int(sqrt(n_nodes))

	empty = 99 # a number not in range [0,15]
	manh = [[empty for x in range(manh_size)] for j in range(manh_size)]

	fixed_nodes = []
	m = 0
	while(len(fixed_nodes)!= n_nodes):
		current_node = total_nodes_traffic[m][1]
		# check if this nodes is already in the manh
		if not(current_node in fixed_nodes):
			# get indeces ii jj of the place in the manh and the list of indeces of its available neighbors
			ii, jj, neighbors = get_best_place(manh_size)
			# put the node in the manh
			manh[ii][jj] = current_node
			fixed_nodes.append(current_node)
			# get the len(neighbors) best neighbors (4, 3, 2, 1 or 0)
			for nn in range(len(neighbors)):
				next = 0
				for a in range(len(joined_f_vector)):
					if next==0: # true if we are still looking for a neighbor 
						# search the neighbor
						if (joined_f_vector[a][1]==current_node):
							# get the potential neighbor
							current_neighbor = joined_f_vector[a][2]
							if not(current_neighbor in fixed_nodes):
								# get the indeces of the neighbor
								p = neighbors[nn][0] # raw
								q = neighbors[nn][1] # column
								manh[p][q] = current_neighbor
								fixed_nodes.append(current_neighbor)
								next = 1
						if (joined_f_vector[a][2]==current_node):
							# get the potential neighbor
							current_neighbor = joined_f_vector[a][1]
							if not(current_neighbor in fixed_nodes):
								# get the indeces of the neighbor
								p = neighbors[nn][0] # raw
								q = neighbors[nn][1] # column
								manh[p][q] = current_neighbor
								fixed_nodes.append(current_neighbor)
								next = 1
		# go to the next node which is exchanging more traffic
		m += 1

	manh_dict = dict()
	for i in range(manh_size):
		for j in range(manh_size):
			manh_dict[ manh[i][j] ] = [i,j] # node_id, row, column

	# the key is the link and the value is the flow: 
	# e.g. flows["0001"] = 5 means from position 00 to position 01 the flow is 5
	flows = dict()

	for v in range(len(f_vector)):
		flow = f_vector[v][0]
		s = f_vector[v][1] # source_id
		d = f_vector[v][2] # dest_id
		s1 = manh_dict[s][0] # row
		s2 = manh_dict[s][1] # column
		d1 = manh_dict[d][0]
		d2 = manh_dict[d][1]

		keys = []
		# check if we are in the same row
		if s1==d1:
			check_row(s2,d1,d2,keys,flow)

		# check if dest_id is one row below
		if (s1+1)%manh_size==d1:
			# down
			keys.append(str(s1) + str(s2) + str(d1) +str(s2))
			check_row(s2,d1,d2,keys,flow)

		# check if dest_id is two rows below
		if (s1+2)%manh_size==d1:
			# down
			keys.append(str(s1) + str(s2) + str((s1+1)%manh_size) +str(s2))
			# down
			keys.append(str((s1+1)%manh_size) +str(s2) + str(d1) + str(s2))
			check_row(s2,d1,d2,keys,flow)

		# check if dest_id is one row above
		if (s1+manh_size-1)%manh_size==d1:
			# up
			keys.append(str(s1) + str(s2) + str((s1+manh_size-1)%manh_size) +str(s2))
			check_row(s2,d1,d2,keys,flow)

	sorted_flows = sorted(flows.items(), key=itemgetter(1))

	for i in range(len(sorted_flows)):
		if i==(len(sorted_flows)-1):
			simulations.append(sorted_flows[i][1])

mean = sum(simulations)/len(simulations)
print str(mean)
