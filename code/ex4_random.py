from __future__ import division
from random import randint
from math import sqrt
from operator import itemgetter

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

	f_vector = []
	for i in range(n_nodes):
		for j in range(n_nodes):
			if t_matrix[i][j] != 0:
				f_vector.append([t_matrix[i][j], i, j])

	manh_size = int(sqrt(n_nodes))

	empty = 99 # a number not in range [0,15]
	manh = [[empty for x in range(manh_size)] for j in range(manh_size)]

	available_nodes = range(n_nodes)

	for i in range(manh_size):
		for j in range(manh_size):
			node = available_nodes[randint(0,len(available_nodes)-1)]
			manh[i][j] = node
			available_nodes.remove(node)

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
