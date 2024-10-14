import pandas as pd
import networkx as nx
from infomap import Infomap

graphs = ["stexpanded", "memoryalpha"]

for graph in graphs:

    print("##################################################")
    print("Reading graph " + graph)
    graph_path = "data/filtered_triples_weighted/" + graph + ".triples"
    graph_df = pd.read_csv(graph_path, sep="###", engine="python")

    G = nx.DiGraph()
    for row in graph_df.itertuples():
        G.add_edge(int(row[1]), int(row[2]), weight=float(row[3]))

    communities_path = ("results/communities_infomap/" + graph + ".csv")

    im = Infomap()

    for u, v, d in G.edges(data=True):
        im.add_link(u, v, d['weight'])

    im.run()

    communities = im.get_modules()

    communities_dict = dict()

    for node, community in communities.items():
        if community not in communities_dict:
            communities_dict[community] = list()
            communities_dict[community].append(node)
        else:
            communities_dict[community].append(node)

    with open(communities_path, 'w') as communities_output:
        for k, v in communities_dict.items():
            communities_output.write(str(v)
                                     .replace("[", "")
                                     .replace("]", "")
                                     .replace(", ", ";") + "\n")

    print("Communities for graph " + graph + " found")
