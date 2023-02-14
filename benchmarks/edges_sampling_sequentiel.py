import networkx as nx
import random
import sys
import sys
sys.path.append('..')
from cl_model import Cl_distribution
import threading
import time

'''
def edge_sampling(graph,m):
    global iter
    while graph.number_of_edges()<m:
        id1 = cl_helper.rvs()
        while graph.degree(id1)>=degree_sequence[id1]:
            id1 = cl_helper.rvs()
        id2 = cl_helper.rvs()
        while graph.degree(id2)>=degree_sequence[id2]:
            id2 = cl_helper.rvs()
        while id1==id2:
            id2 = cl_helper.rvs()
        graph.add_edge(id1,id2)
'''

def edge_sampling(graph,m,cl_helper,degree_sequence):
    iter = 0
    while graph.number_of_edges() < m and iter<10000:
        id1 = cl_helper.rvs()
        if graph.degree(id1)<degree_sequence[id1]:
            id2 = cl_helper.rvs()
            if id2==id1 or graph.degree(id2)>=degree_sequence[id2]:
                continue
            else:
                graph.add_edge(id1,id2)
        iter+=1

def average_clustering(graph, trials=1000):
    triangles = 0
    nodes = graph.nodes()
    for i in [int(random.random() * n) for i in range(trials)]:
        # neighbors of i
        nbrs = list(graph.adj[i])
        if len(nbrs) < 2:
            continue
        u, v = random.sample(nbrs, 2)
        if u in graph[v]:
            triangles +=1
    return triangles / float(trials)

n=int(sys.argv[1])
m=int(sys.argv[2])

# Generate the random original graph
rg = nx.gnm_random_graph(n, m)
degree_sequence = list(d for n, d in rg.degree())

# CL model helper, random sampling fuunction
cl_helper = Cl_distribution(degree_sequence)

# Generate the seed graph
graph_generated = nx.Graph()
for i in range (0,n):
    graph_generated.add_node(i)

start_time = time.time()

edge_sampling(graph_generated,m,cl_helper=cl_helper,degree_sequence=degree_sequence)

end_time = time.time()

print("Elapsed time:", end_time - start_time, "seconds")

value_original = 0
value_generated = 0

for i in range (0,10):
    value_original+=average_clustering(rg,n)
    value_generated+=average_clustering(graph_generated,n)
    
print("number of edges: ",graph_generated.number_of_edges())
print("m: ",m)

print("average clustering coefficient for generated graph: ", value_generated/10)
print("average clustering coefficient for generated graph: ", value_original/10)