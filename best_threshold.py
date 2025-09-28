import json
import statistics
import numpy as np
from tqdm import tqdm


graph_pairs = [
    "mcu-marvel",
    "memoryalpha-memorybeta",
    "stexpanded-memoryalpha",
    "swg-starwars",
    "swtor-starwars"
]

method = "dogtag_nb_summaries_reranked100_deduplicated"
range_min = -10
range_max = 10
steps = 0.1


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


def threshold_found_median(exact_matches, found_pairs):
    found_pairs_nodes = [[item[0], item[1]] for item in found_pairs]
    scores_list = []

    for em in exact_matches:
        if em in found_pairs_nodes:
            for pair in found_pairs:
                if pair[0] == em[0] and pair[1] == em[1]:
                    scores_list.append(float(pair[2]))

    threshold_val = statistics.median(scores_list)
    return threshold_val

for graph_pair in graph_pairs:

    small = graph_pair.split("-")[0]
    big = graph_pair.split("-")[1]

    input_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/" + method + "/" + small + "-" + big + ".json"
    output_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/excel/best_f1/" + method + ".csv"
    best_pairs_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/excel/best_pairs/" + method + "/" + small + "-" + big + ".json"

    gold_pairs_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/gold_pairs/" + small + "-" + big + ".json"
    exact_match_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/exactmatch_deduplicated/" + small + "-" + big + ".json"

    with open(gold_pairs_file) as gpf:
        gold_pairs = json.load(gpf)

    with open(exact_match_file) as emf:
        exact_matches = json.load(emf)

    with open(input_file) as file:
        found_pairs = json.load(file)

    # print("##############################")

    prec, recall, f1, ex_tp, ex_fn, ex_fp = evaluate_preds_extended_discard(gold_pairs, found_pairs)

    # print("no threshold")
    # print("precision:", prec)
    # print("recall:", recall)
    # print("f1:", f1)

    no_prec = prec
    no_recall = recall
    no_f1 = f1

    # print("##############################")

    threshold_median = threshold_found_median(exact_matches, found_pairs)

    output = list()
    for pair in found_pairs:
        if pair[2] >= threshold_median:
            output.append(pair)

    prec, recall, f1, ex_tp, ex_fn, ex_fp = evaluate_preds_extended_discard(gold_pairs, output)

    # print("threshold:", threshold_median)
    # print("precision:", prec)
    # print("recall:", recall)
    # print("f1:", f1)

    original_prec = prec
    original_recall = recall
    original_f1 = f1

    # print("##############################")

    best_t = None
    best_p = None
    best_r = None
    best_f1 = f1
    best_pairs = output

    for t in tqdm(np.arange(range_min, range_max, steps)):

        output = list()
        for pair in found_pairs:
            if pair[2] >= t:
                output.append(pair)

        if len(output) == 0:
            break

        prec, recall, f1, ex_tp, ex_fn, ex_fp = evaluate_preds_extended_discard(gold_pairs, output)

        # print("threshold:", t)
        # print("precision:", prec)
        # print("recall:", recall)
        # print("f1:", f1)

        if f1 > best_f1:
            best_t = t
            best_p = prec
            best_r = recall
            best_f1 = f1
            best_pairs = output

        # print("##############################")

    print("##############################")
    print("######### CONCLUSION #########")
    print("##############################")

    print("original threshold:", threshold_median)
    print("original precision:", original_prec)
    print("original recall:", original_recall)
    print("original f1:", original_f1)

    print("##############################")

    print("no threshold")
    print("no_prec:", no_prec)
    print("no_recall:", no_recall)
    print("no_f1:", no_f1)

    print("##############################")

    print("best threshold:", best_t)
    print("best precision:", best_p)
    print("best recall:", best_r)
    print("best f1:", best_f1)

    with open(output_file, "a") as outfile:
        outfile.write(f"{best_p};{best_r};{best_f1};")

    with open(best_pairs_file, "w") as f:
        json.dump(best_pairs, f, indent=4)
