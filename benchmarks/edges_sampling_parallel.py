import networkx as nx
import random
import sys
import sys
sys.path.append('..')
from cl_model import Cl_distribution
import threading
import time

def edge_sampling_parallel(graph,m,degree_sequence,lock,cl_helper):
    global iter
    while graph.number_of_edges() < m and iter<10000:
        id1 = cl_helper.rvs()
        if graph.degree(id1)<degree_sequence[id1]:
            id2 = cl_helper.rvs()

            if id2==id1 or graph.degree(id2)>=degree_sequence[id2]:
                continue
            else:

                graph.add_edge(id1,id2)
        with lock:
            iter+=1


def edge_sampling_sequentiel(graph,m,degree_sequence,cl_helper):
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


lock = threading.Lock()
threads = []
iter = 0
start_time = time.time()
for i in range(5):
    t = threading.Thread(target=edge_sampling_parallel(graph_generated,m-5,degree_sequence,lock,cl_helper))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

edge_sampling_sequentiel(graph_generated,m,degree_sequence,cl_helper)

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