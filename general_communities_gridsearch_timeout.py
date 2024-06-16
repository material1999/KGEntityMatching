from pytictoc import TicToc
import pandas as pd
import networkx as nx
import statistics
from threading import Timer


def continue_loop():
    global flag_continue
    flag_continue = True


input_graph = "INPUT_GRAPH"
timeout = 1000

max_community_size = 20
connected_percent = [0.4, 0.45, 0.5, 0.55, 0.6]
times_average = [4, 4.5, 5, 5.5, 6]

t = TicToc()
runtimes_path = "runtimes/communities_gridsearch.txt"
with open(runtimes_path, "w") as runtimes_output:
    runtimes_output.write("Runtimes (s) - max_community_size: " + str(max_community_size) +
                          " - timeout (s): " + str(timeout) + "\n")

# Read infection graph file
print("##################################################")
print("Reading input graph: " + input_graph)
graph_path = "data/" + input_graph + ".csv"
G = nx.read_edgelist(graph_path, delimiter="###", data=(('edge_label', str),))
# print(G)

mean_edge_weight = statistics.mean(weight for _, _, weight in G.edges(data='weight'))
# print(mean_edge_weight)

for c_p in connected_percent:
    for t_a in times_average:

        flag_continue = False

        timer = Timer(timeout, continue_loop)
        timer.start()

        t.tic()

        communities = list({i} for i in range(1, 1000 + 1))
        # print(communities)

        print("##################################################")
        print("Parameters - connected_percent: " + str(c_p) + " - times_average: " + str(t_a))
        print("Searching for communities in graph: " + input_graph)
        for community_size in range(2, max_community_size + 1):
            print("Community size: " + str(community_size))
            last_iteration = 0
            to_add = list()
            to_delete = list()
            for community in communities:
                if flag_continue:
                    break
                if len(community) != community_size - 1:
                    continue
                neighbors = set()
                for node in community:
                    neighbors.update(G.neighbors(node))
                    # print(node)
                    # print(neighbors)
                neighbors = [item for item in neighbors if item not in community]
                # print(neighbors)
                for node in neighbors:
                    community_temp = list(community.copy())
                    community_temp.append(node)
                    H = G.subgraph(community_temp)
                    # print(community)
                    # print(community_temp)
                    # print(statistics.mean(weight for _, _, weight in H.edges(data='weight')))
                    # print(len([h for h in H.neighbors(node)]))
                    if statistics.mean(weight for _, _, weight in H.edges(data='weight')) \
                            > mean_edge_weight * t_a and \
                            len([h for h in H.neighbors(node)]) >= (community_size - 1) * c_p:
                        # print("old: " + str(community))
                        # print("new: " + str(community_temp))
                        last_iteration += 1
                        if community not in to_delete:
                            to_delete.append(community)
                        if set(community_temp) not in to_add and set(community_temp) not in communities:
                            to_add.append(set(community_temp))
            if flag_continue:
                break
            if last_iteration == 0:
                print("Break at community size: " + str(community_size))
                break
            # print(to_add)
            # print(to_delete)
            communities = [item for item in communities if item not in to_delete]
            communities.extend(to_add)
            # print(communities)

        if flag_continue:
            print("xxxxxxxxxx")
            with open(runtimes_path, "a") as runtimes_output:
                runtimes_output.write(input_graph + "_" + str(int(c_p * 100)) + "%_" + str(t_a) + "x: "
                                      + "xxxxxxxxxx" + "\n")
            continue

        communities = [item for item in communities if len(item) != 1]
        # print(communities)

        communities_path = ("results/communities_gridsearch/" +
                            input_graph + "_" + str(int(c_p*100)) + "%_" + str(t_a) + "x.csv")
        with open(communities_path, 'w') as communities_output:
            for community in communities:
                communities_output.write(str(community)
                                         .replace("{", "")
                                         .replace("}", "")
                                         .replace(", ", ";") + "\n")

        print("Communities for graph: " + input_graph + " found")
        runtime = t.tocvalue()
        print("Runtime:", runtime, "s")
        with open(runtimes_path, "a") as runtimes_output:
            runtimes_output.write(input_graph + "_" + str(int(c_p*100)) + "%_" + str(t_a) + "x: "
                                  + str(runtime) + "\n")

        timer.cancel()

        # print("##################################################")
