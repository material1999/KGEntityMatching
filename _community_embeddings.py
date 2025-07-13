#%%
import pandas as pd
import numpy as np
import json
#%%
graph = "marvel"
embeddings = "dogtag_bgelarge"
communities = "leiden"
#%%
embeddings_file = "./_input/node_embeddings/" + embeddings + "/" + graph + ".json"
mappings_file = "./_input/mappings/" + graph + ".json"
communities_file = "./_input/communities/" + communities + "/" + graph + ".txt"
community_embeddings_file = "./_input/community_embeddings/" + communities + "_" + embeddings + "/" + graph + ".json"
#%%
df = pd.read_json(embeddings_file)
df_T = df.T
#%%
with open(mappings_file) as file:
    mappings = json.load(file)
    mappings_reversed = {str(v): k for k, v in mappings.items()}
#%%
communities = []
with open(communities_file) as cbf:
    for line in cbf:
        numbers_set = {int(num) for num in line.strip().split(" ")}
        communities.append(numbers_set)
#%%
community_embeddings = []

for community in communities:

    embeddings = []

    for node in community:
        try:
            selected_embedding = df_T.loc[mappings_reversed[str(node)]]
            embeddings.append(selected_embedding)
        except KeyError:
            print(str(node) + " --- Key not found anywhere!")

    community_embedding = np.average(embeddings, axis=0)
    community_embeddings.append(community_embedding)

# embeddings_dict = {
#     str(i): {str(j): val for j, val in enumerate(embedding)}
#     for i, embedding in enumerate(community_embeddings)
# }
embeddings_dict = {
    str(i): list(embedding)
    for i, embedding in enumerate(community_embeddings)
}

with open(community_embeddings_file, "w") as json_file:
    json.dump(embeddings_dict, json_file, indent=4)
#%%
