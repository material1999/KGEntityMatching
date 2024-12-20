#%%
import networkx as nx
import pandas as pd
#%%
graph = "memoryalpha"
community_algorithm = "bigclam"

graph_file = "data/filtered_triples_weighted/" + graph + ".triples"
# communities_file = "./results/communities_" + community_algorithm + "/" + graph + "_10000.txt"
#%%
graph_df = pd.read_csv(graph_file, sep="###", engine="python", header=None)
G = nx.Graph()
for row in graph_df.itertuples():
    G.add_edge(int(row[1]), int(row[2]))
    # G.add_edge(int(row[1]), int(row[2]), weight=int(row[3]))

# communities = []
# with open(communities_file) as cf:
#     for line in cf:
#         numbers_set = {int(num) for num in line.strip().split("\t")}
#         communities.append(numbers_set)
#%%
community_vector = pd.DataFrame({'id': sorted(G.nodes)})
#%%
print("pagerank...")
centrality_dict = nx.pagerank(G)
community_vector['pagerank'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_1.csv", sep=';', index=False)
#%%
print("degree centrality...")
centrality_dict = nx.degree_centrality(G)
community_vector['degree_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_2.csv", sep=';', index=False)
#%%
print("percolation centrality...")
centrality_dict = nx.percolation_centrality(G)
community_vector['percolation_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_3.csv", sep=';', index=False)
#%%
print("closeness centrality...")
centrality_dict = nx.closeness_centrality(G, wf_improved=True)
community_vector['closeness_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_4.csv", sep=';', index=False)
#%%
print("betweenness centrality...")
centrality_dict = nx.betweenness_centrality(G)
community_vector['betweenness_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_5.csv", sep=';', index=False)
#%%
print("harmonic centrality...")
centrality_dict = nx.harmonic_centrality(G)
community_vector['harmonic_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_6.csv", sep=';', index=False)
#%%
print("clustering...")
centrality_dict = nx.clustering(G)
community_vector['clustering'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_7.csv", sep=';', index=False)
#%%
print("eigenvector centrality...")
centrality_dict = nx.eigenvector_centrality(G)
community_vector['eigenvector_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_8.csv", sep=';', index=False)
#%%
print("subgraph centrality...")
centrality_dict = nx.subgraph_centrality(G)
community_vector['subgraph_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_9.csv", sep=';', index=False)
#%%
print("load centrality...")
centrality_dict = nx.load_centrality(G)
community_vector['load_centrality'] = community_vector['id'].map(centrality_dict)
#%%
community_vector.to_csv("results/centrality_vectors/" + graph + "_10.csv", sep=';', index=False)
#%%
# community_vector = pd.read_csv("results/centrality_vectors/" + graph + "_10.csv", sep=';')
#%% md
# # BAD
#%%
# print("current flow betweenness centrality...")
# centrality_dict = nx.current_flow_betweenness_centrality(G)
# community_vector['current_flow_betweenness_centrality'] = community_vector['id'].map(centrality_dict)
#%%
# print("katz centrality...")
# centrality_dict = nx.katz_centrality(G)
# community_vector['katz_centrality'] = community_vector['id'].map(centrality_dict)
#%%
# print("communicability betweenness centrality...")
# centrality_dict = nx.communicability_betweenness_centrality(G)
# community_vector['communicability_betweenness_centrality'] = community_vector['id'].map(centrality_dict)
#%%
# print("information centrality...")
# centrality_dict = nx.information_centrality(G)
# community_vector['information_centrality'] = community_vector['id'].map(centrality_dict)
#%%
# print("second order centrality...")
# centrality_dict = nx.second_order_centrality(G)
# community_vector['second_order_centrality'] = community_vector['id'].map(centrality_dict)
#%%
# print("laplacian centrality...")
# centrality_dict = nx.laplacian_centrality(G)
# community_vector['laplacian_centrality'] = community_vector['id'].map(centrality_dict)