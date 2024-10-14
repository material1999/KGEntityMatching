import pandas as pd
import networkx as nx
from collections import defaultdict
import random
from tqdm import tqdm

#graphs = ["stexpanded", "memoryalpha"]
graphs = ["memoryalpha"]

T = 50  # Number of iterations
r = 0.5  # Threshold for accepting labels
min_size = 2  # Minimum community size (set to 1 to include all, 2 to exclude size 1 communities)


# Function to run SLPA on an undirected, weighted graph
def slpa_undirected_weighted(G, T, r):
    """
    G: A NetworkX undirected and weighted graph
    T: Number of iterations
    r: Threshold for label frequency (to control overlaps)
    """
    # Initialize memory for each node (each node initially holds its own label)
    memory = {node: [node] for node in G.nodes()}

    # Step 1: Iterative Label Propagation
    for t in tqdm(range(T)):
        for node in G.nodes():
            # Node listens to its neighbors' memory and collects weighted labels
            label_counts = defaultdict(float)  # Use float to sum weighted counts

            for neighbor in G.neighbors(node):  # For undirected graph, use neighbors
                chosen_label = random.choice(memory[neighbor])  # Randomly choose a label from the neighbor
                # Get the weight of the edge (default to 1 if no weight is assigned)
                weight = G.get_edge_data(node, neighbor).get('weight', 1.0)
                label_counts[chosen_label] += weight  # Accumulate the weight of the chosen label

            # Node adopts the most frequent label weighted by edge strength
            if label_counts:  # Ensure there are neighbors
                most_frequent_label = max(label_counts, key=label_counts.get)
                memory[node].append(most_frequent_label)

    # Step 2: Post-processing to determine communities
    communities = defaultdict(list)
    for node, labels in memory.items():
        label_frequency = defaultdict(float)
        for label in labels:
            label_frequency[label] += 1

        # Only retain labels that appear with frequency > r
        accepted_labels = [label for label, freq in label_frequency.items() if freq / T >= r]

        # Add node to the corresponding communities
        for label in accepted_labels:
            communities[label].append(node)

    # Step 3: Optionally filter out small communities
    filtered_communities = {label: nodes for label, nodes in communities.items() if len(nodes) >= min_size}

    return filtered_communities


for graph in graphs:

    print("##################################################")
    print("Reading graph " + graph)
    graph_path = "data/filtered_triples_weighted/" + graph + ".triples"
    graph_df = pd.read_csv(graph_path, sep="###", engine="python")

    G = nx.DiGraph()
    for row in graph_df.itertuples():
        G.add_edge(int(row[1]), int(row[2]), weight=float(row[3]))

    communities_path = ("results/communities_slpa/" + graph + ".csv")

    communities_dict = slpa_undirected_weighted(G, T, r)

    with open(communities_path, 'w') as communities_output:
        for k, v in communities_dict.items():
            communities_output.write(str(v)
                                     .replace("[", "")
                                     .replace("]", "")
                                     .replace(", ", ";") + "\n")

    print("Communities for graph " + graph + " found")
