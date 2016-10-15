from __future__ import division
from random import randint
from math import sqrt

# return the indeces of the place in the manh with the highest available number of 
# neighbors and the indeces of these neigbors 
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

n_nodes = 16

# create a random traffic matrix
t_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
for i in range(n_nodes):
	for j in range(n_nodes):
		if j != i:
			t_matrix[i][j] = randint(5, 15)/10

# print"\nt_matrix:"
# for i in range(n_nodes):	
# 	print t_matrix[i]

# join the traffic i-j with traffic j-i (half matrix under the diagonal will be zero)
joined_t_matrix = [[0 for x in range(n_nodes)] for j in range(n_nodes)]
for i in range(n_nodes):
	for j in range(i):
		joined_t_matrix[j][i] = t_matrix[i][j] + t_matrix[j][i]

# print"\njoined_t_matrix:"
# for i in range(n_nodes):	
# 	print joined_t_matrix[i]

joined_f_vector = []
for i in range(n_nodes):
	for j in range(n_nodes):
		if joined_t_matrix[i][j] != 0:
			joined_f_vector.append([joined_t_matrix[i][j], i, j])

joined_f_vector.sort(reverse=True)
print "\nsorted joined_f_vector"
for i in range(len(joined_f_vector)):	
	print joined_f_vector[i]

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
print "\ntotal_nodes_traffic"
for i in range(len(total_nodes_traffic)):
	print total_nodes_traffic[i]

manh_size = int(sqrt(n_nodes))

empty = 99 # a number not in range [0,15]
manh = [[empty for x in range(manh_size)] for j in range(manh_size)]

fixed_nodes = []
m = 0
while(len(fixed_nodes)!= n_nodes):
	print str(len(fixed_nodes))
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

for h in range(manh_size):
	print manh[h]
