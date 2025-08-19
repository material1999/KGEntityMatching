#%%
import json
import torch
from sentence_transformers import util
from transformers import AutoModelForSequenceClassification, AutoTokenizer
#%%
small = "swg"
big = "starwars"
embeddings = "dogtag_bgelarge"
top = 100
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#%%
mappings_file_small = "/hdd/mappings/" + small + ".json"
mappings_file_big = "/hdd/mappings/" + big + ".json"

node_embeddings_small_file = "/hdd/node_embeddings/" + embeddings + "/" + small + ".json"
node_embeddings_big_file = "/hdd/node_embeddings/" + embeddings + "/" + big + ".json"

dogtags_small_file = "/hdd/dogtags/" + small + ".json"
dogtags_big_file = "/hdd/dogtags/" + big + ".json"

exact_match_file = "./_input/exact_match/" + small + "-" + big + ".json"

output_file = "/hdd/found_pairs_em/" + small + "-" + big + ".txt"
#%%
with open(mappings_file_small) as file:
    mappings_small = {str(v): k for k, v in json.load(file).items()}
    mappings_small_reversed = {v: k for k, v in mappings_small.items()}

with open(mappings_file_big) as file:
    mappings_big = {str(v): k for k, v in json.load(file).items()}
    mappings_big_reversed = {v: k for k, v in mappings_big.items()}

with open(node_embeddings_small_file) as nesf:
    node_embeddings_small = json.load(nesf)
    node_embeddings_small = {mappings_small_reversed[k]: v for k, v in node_embeddings_small.items()}

with open(node_embeddings_big_file) as nebf:
    node_embeddings_big = json.load(nebf)
    node_embeddings_big = {mappings_big_reversed[k]: v for k, v in node_embeddings_big.items()}

with open(dogtags_small_file) as df:
    dogtags_small = json.load(df)

with open(dogtags_big_file) as df:
    dogtags_big = json.load(df)

with open(exact_match_file) as file:
    exact_match = json.load(file)
#%%
node_embeddings_small_list = list()
node_ids_small_list = list()

node_embeddings_big_list = list()
node_ids_big_list = list()

for k, v in node_embeddings_small.items():
    node_ids_small_list.append(k)
    node_embeddings_small_list.append(v)

for k, v in node_embeddings_big.items():
    node_ids_big_list.append(k)
    node_embeddings_big_list.append(v)

with open(exact_match_file) as file:
    exact_match = json.load(file)
#%%
tensor_small = torch.Tensor(node_embeddings_small_list).to(device)
tensor_big = torch.Tensor(node_embeddings_big_list).to(device)
node_order = util.semantic_search(tensor_small, tensor_big, top_k=top)
#%%
top_dict = dict()
for idx, (node_id, order) in enumerate(zip(node_ids_small_list, node_order)):
    items_list = list()
    for item in order:
        items_list.append((node_ids_big_list[item['corpus_id']], item['score']))
    top_dict[node_id] = items_list
#%%
for em in exact_match:
    if str(em[0]) in top_dict:
        bool_append = True
        for item in top_dict[str(em[0])]:
            if item[0] == str(em[1]):
                bool_append = False
                break
        if bool_append:
            top_dict[str(em[0])].append((str(em[1]), 1.0))
#%%
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large')
model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')
model.to(device)
model.eval()
#%%
with open(output_file, "w") as file:
    for node in node_ids_small_list:
        id_list = list()
        str_list = list()
        for i in range(0, top):
            id_list.append(top_dict[node][i][0])
            str_list.append(
                [
                    str(dogtags_small[mappings_small[node]]),
                    str(dogtags_big[mappings_big[top_dict[node][i][0]]])
                ]
            )

        pairs = str_list
        with torch.no_grad():
            inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512).to(device)
            scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
            # print(scores)

        max_index = torch.argmax(scores)
        max_index_int = int(max_index.item())
        max_value = scores[max_index]
        max_value_float = float(max_value.item())

        file.write(
            mappings_small[node] + "###" +
            mappings_big[id_list[max_index_int]] + "###" +
            str(max_value_float) + "\n"
        )
        file.flush()
#%%
