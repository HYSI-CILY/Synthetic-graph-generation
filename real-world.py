import networkx as nx
import random
import sys
import sys
sys.path.append('..')
from cl_model import Cl_distribution
import time
import numpy as np
from scipy.sparse import csr_matrix

# The two functions below generate an instance of the Chung-Lu random graph model with expected degree sequence w

def make_sparse_adj_matrix(w):
    # Outputs the scipy.sparse adjacency matrix of the graph
    n = np.size(w)
    s = np.sum(w)
    m = ( np.dot(w,w)/s )**2 + s
    m = int(m/2)
    wsum = np.cumsum(w)
    wsum = np.insert(wsum,0,0)
    wsum = wsum / wsum[-1]
    I = np.digitize(np.random.rand(m,1),wsum)
    J = np.digitize(np.random.rand(m,1),wsum)
    row_ind = np.append(I.reshape(m,)-1,J.reshape(m,)-1)
    col_ind = np.append(J.reshape(m,1)-1,I.reshape(m,)-1)
    ones = [1 for i in range(2*m)]    
    A = csr_matrix((ones, (row_ind,col_ind)), shape=(n,n))
    A.data.fill(1)
    return A


def make_nx_graph(w):
    # Outputs the networkx.Graph of the graph
    n = np.size(w)
    s = np.sum(w)
    m = ( np.dot(w,w)/s )**2 + s
    m = int(m/2)
    wsum = np.cumsum(w)
    wsum = np.insert(wsum,0,0)
    wsum = wsum / wsum[-1]
    I = np.digitize(np.random.rand(m,1),wsum)
    J = np.digitize(np.random.rand(m,1),wsum)
    G = nx.Graph()
    G.add_nodes_from(range(1,n+1))
    G.add_edges_from(tuple(zip(I.reshape(m,),J.reshape(m,))))
    return G

def edge_sampling(graph,m,cl_helper,degree_sequence):
    iter = 0
    max = 0.5*mean2(degree_sequence)*mean2(degree_sequence)
    while graph.number_of_edges() < m and iter<max:
        id1 = cl_helper.rvs()
        if graph.degree(id1)<degree_sequence[id1]:
            id2 = cl_helper.rvs()
            if id2==id1 or graph.degree(id2)>=degree_sequence[id2]:
                continue
            else:
                graph.add_edge(id1,id2)
        iter+=1


def edge_sampling2(graph,m,cl_helper,degree_sequence):
    max = (0.5*mean2(degree_sequence)*mean2(degree_sequence))+m
    print("max of iteration: ",max)
    p = cl_helper.cdf()
    for i in range (round(max)):
        #id1 = cl_helper.rvs(p)
        #id2 = cl_helper.rvs(p)
        id1 = np.digitize(np.random.rand(),p)
        id2 = np.digitize(np.random.rand(),p)
        #if id1==id2:
        #    continue
        #else:
        graph.add_edge(id1,id2)
'''
def average_clustering(graph, trials=1000):
    triangles = 0
    for i in [int(random.random() * n) for i in range(1,trials)]:
        # neighbors of i
        nbrs = list(graph.adj[i])
        if len(nbrs) < 2:
            continue
        u, v = random.sample(nbrs, 2)
        if u in graph[v]:
            triangles +=1
    return triangles / float(trials)
'''
def degree_sequence_laplace(degree_sequence,epsilon):
    mean = 0
    scale = 2/epsilon
    size = len(degree_sequence)
    random_variables = np.random.laplace(mean, scale, size)
    list = [0]*size
    for i in range(size):
        list[i] = round(degree_sequence[i]+random_variables[i])
    #print("laplace variables: ",random_variables)
    print("degree sequence with laplace: ",list)
    return list

def calcul_mkj(degree_sequence_noisy,i,j):
        sum = 0
        for k in range (i,j+1):
            sum += (degree_sequence_noisy[k]/(j-i+1))
        return sum

def degree_sequence_contrainte(degree_sequence,epsilon):
    size = len(degree_sequence)
    # sort degree sequence
    #print("degree sequence: ",degree_sequence)
    original_order = [(degree_sequence[i], i) for i in range(size)]
    #print(original_order)
    original_order.sort()
    sorted_list=[]
    orders = []
    for element in original_order:
        sorted_list.append(element[0])
        orders.append(element[1])
    #print("orders: ",orders)
    #print("degree sequence increasing: ",sorted_list)

    mean = 0
    scale = 2/epsilon
    
    random_variables = np.random.laplace(mean, scale, size)
    degree_sequence_noisy = [0]*size
    for i in range (size):
        degree_sequence_noisy[i] = sorted_list[i] + random_variables[i]

    degree_sequence_contrainte = [0]*size
    m_k = [0]*size
    for k in reversed(range(size)):
        candidate_list = []
        for j in range (k,size):
            m_kj = calcul_mkj(degree_sequence_noisy,k,j)
            candidate_list.append(m_kj)
        m_k[k] = min(candidate_list)

    for i in range(size):
        degree_sequence_contrainte[i] = round(max(m_k[:i+1]))
    #print(degree_sequence_contrainte)
    shuffled_degree_sequence_constrainte = [0]*size
    for i in range(len(orders)):
        shuffled_degree_sequence_constrainte[orders[i]] = degree_sequence_contrainte[i]
    print("degree sequence constrained: ",shuffled_degree_sequence_constrainte)
    return shuffled_degree_sequence_constrainte

def mse (list1,list2):
    size = len(list1)
    mse = 0
    for i in range (size):
        mse+=(list1[i]-list2[i])*(list1[i]-list2[i])
    return mse/size

def graph_generation_cl(degree_sequence):
    # CL model helper, random sampling fuunction
    cl_helper = Cl_distribution(degree_sequence)
    # Generate the seed graph
    graph_generated = nx.DiGraph()

    for i in range (0,n):
        graph_generated.add_node(i)

    #edge_sampling(graph_generated,m,cl_helper=cl_helper,degree_sequence=degree_sequence)
    edge_sampling2(graph_generated,m,cl_helper=cl_helper,degree_sequence=degree_sequence)
    return graph_generated

def mean2(degree_sequence):
    size = len(degree_sequence)
    val1 = 0
    val2 = 0
    for i in range (size):
        val1+=degree_sequence[i]*degree_sequence[i]
        val2+=degree_sequence[i]
    return val1/val2

def load_graph(n,filename):
    graph = nx.Graph()
    for i in range (1,n+1):
        graph.add_node(i)
    with open(filename) as f:
        for line in f:
            values = line.split()
            node_i = int(values[0])
            node_j = int(values[1])
            graph.add_edge(node_i+1,node_j+1)
    return graph

n=4039
m=88234
cc=0.6055

g_original = load_graph(4039,"facebook_combined.txt")
degree_sequence = list(d for n, d in g_original.degree())
print(g_original.number_of_edges())
#print(degree_sequence)
#generated_graph = graph_generation_cl(degree_sequence)
start_time = time.time()
generated_graph = make_nx_graph(degree_sequence)
end_time = time.time()
print("Time for FCL: ",end_time-start_time)
degree_sequence_generated = list(d for n, d in generated_graph.degree())
print(generated_graph.number_of_edges())
#print(degree_sequence_generated)
mse1 = mse(degree_sequence,degree_sequence_generated)
print("generated graph degree sequence mse for FCL: ",mse1)
cc_generated = nx.average_clustering(generated_graph)
print("relative error for average clustering coefficient: ",cc_generated)