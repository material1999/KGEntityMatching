#%%
import json
from tqdm import tqdm
import networkx as nx
import pandas as pd
#%%
graph = "memoryalpha"
communities_file = "results/communities_bigclam_new/" + graph + "_10000.txt"
graph_file = "data/filtered_triples/" + graph + ".triples"
mappings_file = "data/triples_v2/" + str(graph) + "_mapping.json"
top_betweenness_file = "results/top_betweenness_bigclam/" + graph + ".json"
# k = 1000
#%%
graph_df = pd.read_csv(graph_file, sep="###", engine="python", header=None)
G_nx = nx.Graph()
for row in graph_df.itertuples():
    G_nx.add_edge(int(row[1]), int(row[2]))
print(G_nx)
#%%
with open(communities_file, 'r') as communities_input, open(mappings_file, "r") as mappings_input:
    print("Processing graph " + graph)
    mappings = json.load(mappings_input)
    results = []
    for line in tqdm(communities_input):
        # entities = [int(e) for e in line.strip().split(" ")]
        entities = [int(e) for e in line.strip().split("\t")]
        G = G_nx.subgraph(entities)
        # if len(G.nodes) > k:
        #     betweenness = nx.betweenness_centrality(G, k=k)
        # else:
        #     betweenness = nx.betweenness_centrality(G)
        betweenness = nx.betweenness_centrality(G)
        top_100_betweenness = dict(sorted(betweenness.items(), key=lambda item: item[1], reverse=True)[:100])
        results.append(top_100_betweenness)

with open(top_betweenness_file, "w") as f:
    json.dump(results, f, indent=4)
#%%
