import pandas as pd

# graphs = ["stexpanded", "memoryalpha"]
graphs = ["swtor", "swg", "memorybeta", "marvel", "mcu", "starwars"]

for graph in graphs:

    df = pd.read_csv("data/filtered_triples_weighted/" + graph + ".triples", delimiter='###', header=None,
                     engine='python')

    with open("data/other/" + graph + ".txt", 'w') as f:
        f.write("# Directed Node Graph \n")
        f.write("# Autonomous systems (graph is undirected, only first two numbers from each row)\n")
        f.write(f"# Nodes: {pd.concat([df[0], df[1]]).nunique()}    Edges: {df.shape[0]}\n")
        f.write("# SrcNId\tDstNId\n")

        for _, row in df.iterrows():
            f.write(f"{row[0]}\t{row[1]}\n")
