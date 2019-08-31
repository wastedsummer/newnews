import numpy as np


def euclidean_distance(u,v):
	# print(u)
	# print(v)
	return np.sqrt(sum([(u[i]-v[i])**2 for i in range(len(u))]))

def cosine_distance(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def normalize(v):
	return v/np.linalg.norm(v)

def mag(v): 
    return np.sqrt(sum([i**2 for i in v]))


