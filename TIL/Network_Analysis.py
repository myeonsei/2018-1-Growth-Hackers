from collections import deque
from pprint import pprint
import numpy as np
from numpy import linalg as LA

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

for user in users:
    user["friends"] = []
    
for i, j in friendships:
    users[i]["friends"].append(users[j])
    users[j]["friends"].append(users[i]) 

def degree_centrality(users, user_id):
	numerator = len(users[user_id]["friends"])
	denominator = 0
	for user in users:
		denominator += len(user["friends"])

	return numerator / denominator

def shortest_paths_from(from_user):
	shortest_paths_to = {from_user["id"] : [[]]}
	frontier = deque((from_user, friend) for friend in from_user["friends"])

	while frontier: # frontier에 아무 것도 안 남을 떄까지.
		prev_user, user = frontier.popleft()
		user_id = user["id"]

		paths_to_prev_user = shortest_paths_to[prev_user["id"]]
		new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]
		old_paths_to_user = shortest_paths_to.get(user_id, [])

		if old_paths_to_user:
			old_min_path_length = len(min(old_paths_to_user, key = lambda x : len(x)))

		else:
			old_min_path_length = float("inf")

		new_min_path_length = len(min(new_paths_to_user, key = lambda x : len(x)))

		if new_min_path_length < old_min_path_length:
			shortest_paths_to[user_id] = [path for path in new_paths_to_user \
										  if len(path) == new_min_path_length]

		elif new_min_path_length == old_min_path_length:
			new_paths_to_user = [path for path in new_paths_to_user \
								 if len(path) == new_min_path_length \
								 and path not in old_paths_to_user]
			shortest_paths_to[user_id] = old_paths_to_user + new_paths_to_user

		else:
			pass

		frontier.extend((user,friend) for friend in user["friends"] \
						 if friend["id"] not in shortest_paths_to)
        
	return shortest_paths_to

pprint(shortest_paths_from(users[0]))

for user in users:
	user["shortest_paths"] = shortest_paths_from(user)
	user["betweenness_centrality"] = 0.0

for source in users:
	source_id = source["id"]

	for target_id, paths in source["shortest_paths"].items():
		if source_id < target_id:
			num_paths = len(paths)
			contrib = 1 / num_paths
			for path in paths:
				for id in path[:-1]:
					users[id]["betweenness_centrality"] += contrib

def farness(user):
	# user는 users[0]와 같은 형태.
	return sum(len(paths[0]) for paths \
				in user["shortest_paths"].values())

for user in users:
	user["closeness_centrality"] = 1 / farness(user)

adj_matrix = np.zeros((len(users),len(users)))

for i, j in friendships:
	adj_matrix[i][j] = 1
	adj_matrix[j][i] = 1

w, v = LA.eig(adj_matrix)

for user_id, eigenvector_centrality in enumerate(-v[:,0]):
    users[user_id]["eigenvector_centrality"] = eigenvector_centrality
