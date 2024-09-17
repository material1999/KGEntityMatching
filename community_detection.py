import pandas as pd
import networkx as nx
import numpy as np
from pytictoc import TicToc

graph = "stexpanded"
max_community_size = 50
connected_percent = 0.75
times_average = 1.5

t = TicToc()
t.tic()

print("Reading graph " + str(graph))
graph_path = "./data/filtered_triples_weighted/"
graph_df = pd.read_csv(graph_path + graph + ".triples", sep="###", engine="python", header=None)
G = nx.Graph()
for row in graph_df.itertuples():
    G.add_edge(int(row[1]), int(row[2]), weight=int(row[3]))

print(G)

mean_edge_weight = np.mean([weight for _, _, weight in G.edges(data='weight')])

communities_path = "./data/communities/"
communities = {frozenset([i]) for i in G.nodes}
to_add = {frozenset([i]) for i in G.nodes}

print("Parameters - connected_percent: " + str(connected_percent) + " - times_average: " + str(times_average))
print("Searching for communities in graph " + graph)

for community_size in range(2, max_community_size + 1):

    print("Community size: " + str(community_size))
    last_iteration = 0
    communities_to_test = to_add.copy()
    to_add.clear()
    count = 0
    number_to_test = len(communities_to_test)
    print("Number of communities to test: " + str(number_to_test))

    for community in communities_to_test:
        is_expanded = False
        count += 1
        if count % 1000 == 0:
            print(str(count) + "/" + str(number_to_test))
        neighbors = set()
        for node in community:
            neighbors.update(G.neighbors(node))
        neighbors -= community
        for node in neighbors:
            community_temp = community.union([node])
            H = G.subgraph(community_temp)
            if len(H[node]) >= (community_size - 1) * connected_percent and \
                    np.mean([weight for _, _, weight in H.edges(data='weight')]) > mean_edge_weight * times_average:
                last_iteration += 1
                to_add.add(community_temp)
                if not is_expanded:
                    communities.remove(community)
                    is_expanded = True

    if community_size == 2:
        communities = [item for item in communities if len(item) != 1]

    if last_iteration == 0:
        print("Break at community size: " + str(community_size))
        break

    communities.extend(to_add)
    print("Total communities: " + str(len(communities)))

with open(communities_path + graph + ".csv", 'w') as communities_output:
    for community in communities:
        communities_output.write(str(community)
                                 .replace("frozenset({", "")
                                 .replace("})", "")
                                 .replace(", ", ";") + "\n")

print("Communities for graph " + graph + " found: " + str(len(communities)))

runtime = t.tocvalue()
print("Runtime:", runtime, "s")
