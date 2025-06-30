from sentence_transformers import SentenceTransformer
import os
import json
from tqdm import tqdm

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
gpu = False
bge_large = "BAAI/bge-large-en-v1.5"

# graphs = ["stexpanded"]
# graphs = ["stexpanded", "memoryalpha"]
# graphs = ["swtor", "swg", "memorybeta", "mcu", "starwars", "marvel"]
graphs = ["starwars", "marvel"]
mappings_path = "_input/mappings/"
dogtags_path = "_input/dogtags_mate/"
embeddings_output_path = "_input/edgetype_embeddings/dogtag_bgelarge/"


def get_mappings(graph_name):
    with open(mappings_path + graph_name + ".json") as mf:
        mappings = json.load(mf)
        mappings_dict = {key: value for key, value in mappings.items()}
        return mappings_dict


def get_dogtags(graph_name):
    with open(dogtags_path + graph_name + ".json") as df:
        dogtags = json.load(df)
        dogtags_dict = {key: value for key, value in dogtags.items()}
        return dogtags_dict


def get_edgetypes(mappings, dogtags):
    edgetypes = dict()
    for key, value in dogtags.items():
        value_str = '\n'.join(f'{k}: {v}' for k, v in value.items())
        value_new = "; ".join(
            [item.strip().split(":")[0] for item in value_str.split("\n")]
        )
        edgetypes[mappings[key]] = value_new
    return edgetypes


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


def write_embeddings(graph_name, embeddings):
    graph_name += ".json"
    with open(os.path.join(embeddings_output_path, graph_name), "w") as f:
        json.dump(embeddings, f)


selected_embedder = bge_large
print("Model:", selected_embedder)

for g in graphs:
    print(g)
    mappings = get_mappings(g)
    dogtags = get_dogtags(g)
    edgetypes = get_edgetypes(mappings, dogtags)
    print("Edgetypes created")
    embeddings = sentence_embed(edgetypes, model_name=selected_embedder, gpu=gpu)
    print("Writing embeddings...")
    write_embeddings(g, embeddings)
    print("Done...")
