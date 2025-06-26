from sentence_transformers import SentenceTransformer
import os
import json
from tqdm import tqdm
from itertools import islice

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
gpu = False
bge_large = "BAAI/bge-large-en-v1.5"

# graphs = ["stexpanded"]
graphs = ["memoryalpha", "swtor", "swg", "memorybeta", "mcu", "starwars", "marvel"]
graph_path = "data/triples_v2/"
embeddings_output_path = "results/url_embeddings_short/"

exclusions = [".jpg", ".jpeg", ".png", ".gif"]
types = ["/property/", "/resource/", "/class/", "/ontology/"]


def get_mappings(graph_name):
    with open(graph_path + graph_name + "_mapping.json") as mf:
        mappings = json.load(mf)
        mappings_dict = {value: key for key, value in mappings.items()}
        return mappings_dict


def get_urls(mappings):
    urls = dict()
    for key, value in mappings.items():
        if value.startswith("http"):
            if all(item not in value for item in exclusions):
                if any(item in value for item in types):
                    matching_item = next((item for item in types if item in value), None)
                    urls[key] = value.split(matching_item)[1]
                elif "#" in value:
                    urls[key] = value.split("#")[1]
                elif "/" in value:
                    urls[key] = value.split("/")[-1]
                else:
                    urls[key] = value
    return urls


def sentence_embed(dogtags, model_name="dunzhang/stella_en_400M_v5", gpu=False):
    if gpu:
        model = SentenceTransformer(model_name, trust_remote_code=True, device="cuda").cuda()
    else:
        model = SentenceTransformer(model_name, trust_remote_code=True, device="cpu")

    embeddings = dict()
    for key, dt in tqdm(dogtags.items()):
        query_embedding = model.encode(dt).tolist()
        embeddings[key] = query_embedding
    return embeddings


def write_embeddings(graph_name, embeddings, extra_identifier=""):
    if extra_identifier is not None:
        graph_name += f"_{extra_identifier}"
    graph_name = graph_name.replace("/", "_")
    graph_name += ".json"

    with open(os.path.join(embeddings_output_path, graph_name), "w") as f:
        json.dump(embeddings, f)


selected_embedder = bge_large
print("Model:", selected_embedder)

for g in graphs:
    print(g)
    mappings = get_mappings(g)
    urls = get_urls(mappings)
    print("URLs created")
    embeddings = sentence_embed(urls, model_name=selected_embedder, gpu=gpu)
    print("Writing embeddings...")
    write_embeddings(g, embeddings, f"url_{selected_embedder}")
    print("Done...")
