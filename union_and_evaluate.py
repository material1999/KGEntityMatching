import json


graph_pairs = [
    "mcu-marvel",
    "memoryalpha-memorybeta",
    "stexpanded-memoryalpha",
    "swg-starwars",
    "swtor-starwars"
]

method = "dogtag_short_reranked100_deduplicated"


def get_tp(golds, preds):
    tps = list()
    remaining = list()
    for pred in preds:
        found = False
        for gold in golds:
            if gold[0] == pred[0] and gold[1] == pred[1]:
                found = True
                tps.append(pred)
                break
        if found is False:
            remaining.append(pred)
    return tps, remaining


def get_fn(golds, preds):
    fns = list()
    for gold in golds:
        found = False
        for pred in preds:
            if gold[0] == pred[0] and gold[1] == pred[1]:
                found = True
                break
        if found is False:
            fns.append(gold)
    return fns


def get_fp(golds, preds):
    fps = list()
    remaining = list()
    for pred in preds:
        found = False
        for gold in golds:
            if (gold[0] == pred[0] and gold[1] != pred[1]) or (gold[0] != pred[0] and gold[1] == pred[1]):
                found = True
                fps.append(pred)
                break
        if found is False:
            remaining.append(pred)
    return fps, remaining


def discard_preds(preds, golds):
    gold1 = {element[0] for element in golds}
    gold2 = {element[1] for element in golds}

    returnables = list()
    for pair in preds:
        if pair[0] in gold1 or pair[1] in gold2:
            returnables.append(pair)
    return returnables


def evaluate_preds(golds, preds):
    return evaluate_preds_extended(golds, preds)[:3]


def evaluate_preds_extended_discard(golds, preds):
    preds_discarded = discard_preds(preds, golds)

    fns = get_fn(golds, preds_discarded)
    tps, remaining = get_tp(golds, preds_discarded)
    fps, remaining2 = get_fp(golds, remaining)

    precision = len(tps) / (len(tps) + len(fps))
    recall = len(tps) / (len(tps) + len(fns))
    f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1, tps, fns, fps


def evaluate_preds_extended(golds, preds):
    fns = get_fn(golds, preds)
    tps, remaining = get_tp(golds, preds)
    fps, remaining2 = get_fp(golds, remaining)

    precision = len(tps) / (len(tps) + len(fps))
    recall = len(tps) / (len(tps) + len(fns))
    f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1, tps, fns, fps


def union_em_found(exact_match, found_pairs):

    exact_match_left = {em[0] for em in exact_match}
    output = list()

    for em in exact_match:
        output.append(em)

    for pair in found_pairs:
        if pair[0] not in exact_match_left:
            output.append(pair)

    return output

for graph_pair in graph_pairs:

    small = graph_pair.split("-")[0]
    big = graph_pair.split("-")[1]

    best_pairs_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/excel/best_pairs/" + method + "/" + small + "-" + big + ".json"
    output_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/excel/best_f1_union/" + method + ".csv"

    gold_pairs_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/gold_pairs/" + small + "-" + big + ".json"
    exact_match_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/exactmatch_deduplicated/" + small + "-" + big + ".json"

    with open(gold_pairs_file) as gpf:
        gold_pairs = json.load(gpf)

    with open(exact_match_file) as emf:
        exact_matches = json.load(emf)

    with open(best_pairs_file) as file:
        best_pairs = json.load(file)

    union_best_pairs = union_em_found(exact_matches, best_pairs)

    prec, recall, f1, ex_tp, ex_fn, ex_fp = evaluate_preds_extended_discard(gold_pairs, union_best_pairs)

    # print("##############################")

    with open(output_file, "a") as outfile:
        outfile.write(f"{prec};{recall};{f1};")
