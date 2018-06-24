## K-Means Hard Coding

from linear_algebra import squared_distance, vector_mean, distance
import math, random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class KMeans:
    def __init__(self, k):
        self.k = k
        self.means = None; self.assignments = None
        
    def classify(self, input_):
        return min(range(self.k), key=lambda i: squared_distance(input_, self.means[i]))

    def train(self, inputs):
        self.means = random.sample(inputs, self.k)
        self.assignments = None

        while True:
            new_assignments = list(map(self.classify, inputs))

            if self.assignments == new_assignments:
                return

            self.assignments = new_assignments

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, self.assignments) if a == i]
                if i_points:
                    self.means[i] = vector_mean(i_points)
                    
inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]
random.seed(42)
clusterer = KMeans(3)
clusterer.train(inputs)

for i in range(len(inputs)):
    x, y = inputs[i]
    if clusterer.assignments[i] == 0:
        plt.scatter(x, y, marker = 'D', color = 'r')
    elif clusterer.assignments[i] == 1:
        plt.scatter(x, y, marker = 'o', color = 'g')
    else:
        plt.scatter(x, y, marker = '*', color = 'b')

# Finding Optimal K

def squared_clustering_errors(inputs, k):
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = list(map(clusterer.classify, inputs))

    return sum(squared_distance(input_,means[cluster]) for input_, cluster in zip(inputs, assignments))

def plot_squared_clustering_errors(inputs):
    ks = range(1, len(inputs) + 1)
    errors = [squared_clustering_errors(inputs, k) for k in ks]

    plt.plot(ks, errors)
    plt.xticks(ks)
    plt.xlabel("k")
    plt.ylabel("total squared error")
    plt.show()
    
# Hierarchy Clustering Hard Coding
    
def is_leaf(cluster):
    return len(cluster) == 1

def get_children(cluster):
    if is_leaf(cluster):
        raise TypeError("a leaf cluster has no children")
    else:
        return cluster[1]

def get_values(cluster):
    if is_leaf(cluster):
        return cluster
    else:
        return [value for child in get_children(cluster) for value in get_values(child)]

def cluster_distance(cluster1, cluster2, distance_agg=min):
    return distance_agg([distance(input1, input2) for input1 in get_values(cluster1) for input2 in get_values(cluster2)])

def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0]

def bottom_up_cluster(inputs, distance_agg=min):
    clusters = [(input_,) for input_ in inputs]

    while len(clusters) > 1:
        c1, c2 = min([(cluster1, cluster2)\
                     for i, cluster1 in enumerate(clusters)\
                     for cluster2 in clusters[:i]],\
                     key=lambda p: cluster_distance(p[0], p[1], distance_agg))

        clusters = [c for c in clusters if c != c1 and c != c2]
        merged_cluster = (len(clusters), [c1, c2])
        clusters.append(merged_cluster)
    return clusters[0]

def generate_clusters(base_cluster, num_clusters):
    clusters = [base_cluster]

    while len(clusters) < num_clusters:
        next_cluster = min(clusters, key=get_merge_order)
        clusters = [c for c in clusters if c != next_cluster]
        clusters.extend(get_children(next_cluster))

    return clusters
