import json
from tqdm import tqdm

communities_path = "./data/communities/"
mappings_path = "./data/triples_v2/"
communities_formatted_path = "./data/communities_formatted/"
one_step_path = "./data/one_step/"
one_step_formatted_path = "./data/one_step_formatted/"

graph = "starwars"

'''
with open(communities_path + graph + ".csv", 'r') as communities_input, open(communities_formatted_path + graph + ".csv", 'w') as communities_output, open(mappings_path + str(graph) + "_mapping.json", "r") as m:
    print("Processing graph " + graph)
    mapping = json.load(m)
    for line in tqdm(communities_input):
        entities = line.strip().split(";")
        for entity in entities:
            key = str(next((key for key, value in mapping.items() if str(value) == entity), None))
            communities_output.write(key + "\n")
        communities_output.write("##################################################\n")
'''

with open(one_step_path + graph + ".csv", 'r') as one_step_input, open(one_step_formatted_path + graph + ".csv", 'w') as one_step_output, open(mappings_path + str(graph) + "_mapping.json", "r") as m:
    print("Processing graph " + graph)
    mapping = json.load(m)
    for line in tqdm(one_step_input):
        entities = line.strip().split(";")
        for entity in entities:
            key = str(next((key for key, value in mapping.items() if str(value) == entity), None))
            one_step_output.write(key + "\n")
        one_step_output.write("##################################################\n")
