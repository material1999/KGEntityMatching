#%%
import pandas as pd
import numpy as np
import json
import networkx as nx
from tqdm import tqdm
#%%
graph = "marvel"
embeddings = "dogtag_bgelarge"
#%%
embeddings_file = "./_input/node_embeddings/" + embeddings + "/" + graph + ".json"
graph_file = "_input/triples/" + graph + ".triples"
mappings_file = "./_input/mappings/" + graph + ".json"
neighborhood_embeddings_file = "./_input/neighborhood_embeddings/" + embeddings + "/" + graph + ".json"
#%%
with open(mappings_file) as file:
    mappings = json.load(file)
    mappings_reversed = {str(v): k for k, v in mappings.items()}
#%%
df = pd.read_json(embeddings_file)
df_T = df.T
#%%
graph_df = pd.read_csv(graph_file, sep="###", engine="python", header=None)
G_nx = nx.Graph()
for row in graph_df.itertuples():
    G_nx.add_edge(int(row[1]), int(row[2]))
print(G_nx)
#%%
embeddings_dict = dict()

for n in tqdm(G_nx.nodes):
    
    neighbors = nx.neighbors(G_nx, int(n))
    embeddings = []

    selected_embedding = df_T.loc[mappings_reversed[str(n)]]
    embeddings.append(selected_embedding)

    for node in neighbors:
        selected_embedding = df_T.loc[mappings_reversed[str(node)]]
        embeddings.append(selected_embedding)

    neighborhood_embedding = np.average(embeddings, axis=0)
    embeddings_dict.update({n: list(neighborhood_embedding)})

with open(neighborhood_embeddings_file, "w") as json_file:
    json.dump(embeddings_dict, json_file, indent=4)
#%%
