# importing the required module
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import pygenstability as pgs
import pickle

# import data set
final_network = pd.read_csv('./Final_Network_Data.csv', index_col = 0)

# create bipartite graph using networkx
g_follow = nx.Graph()

for _, row in final_network.iterrows():
    g_follow.add_node(row['Source'], bipartite=0)  # Add source node to partite set 0
    g_follow.add_node(row['Target'], bipartite=1)  # Add target node to partite set 1
    g_follow.add_edge(row['Source'], row['Target'])

target_nodes = {node for node, bipartite in g_follow.nodes(data='bipartite') if bipartite == 1}

# project the bipartite graph on the influencer side
g_projected = bipartite.weighted_projected_graph(g_follow, target_nodes)

# select the largest component in the projected graph
components = list(nx.connected_components(g_projected))
largest_component = max(components, key=len)
g_largest = g_projected.subgraph(largest_component)

# run Pygenstability valuations for the largest component

## 1. convert the graph to a sparse matrix
sparse_matrix = nx.to_scipy_sparse_array(g_largest)

## 2. run markov stability and identify optimal scales
results = pgs.run(
    sparse_matrix,
    method = "leiden",  ## optimiation method
    min_scale=-3,  ## the range of resolution parameters
    max_scale=3,
    n_scale=1000,
    n_tries=100,
    constructor= "linearized", # continuous_normalized, linearized
    n_workers=4, ## number of workers for multiprocessing
)

# save the results
file_path1 = './graph.pkl'
file_path2 = './results_n_scales1000.pkl'

with open(file_path1, 'wb') as file:
    pickle.dump(g_largest, file)

with open(file_path2, 'wb') as file:
    pickle.dump(results, file)