#%%
import json
from urllib.parse import quote
#%%
small = "swg"
big = "starwars"

method_1_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results_union/union_dogtag_long_top1/" + small + "-" + big + ".json"
method_2_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results_union/union_dogtag_long_top10pairs_llm_strict_deduplicated/" + small + "-" + big + ".json"

gold_pairs_file = "/Users/matevass/Documents/Projects/KGEntityMatching-Public/results/gold_pairs/" + small + "-" + big + ".json"

dogtags_small_file = "/Users/matevass/Documents/Projects/KGEntityMatching/_input/dogtags/" + small + ".json"
dogtags_big_file = "/Users/matevass/Documents/Projects/KGEntityMatching/_input/dogtags/" + big + ".json"
#%%
with open(gold_pairs_file) as gpf:
    gold_pairs = json.load(gpf)

with open(method_1_file) as m1f:
    method_1 = [[item[0], item[1]] for item in json.load(m1f)]

with open(method_2_file) as m2f:
    method_2 = [[item[0], item[1]] for item in json.load(m2f)]

with open(dogtags_small_file) as dsf:
    dogtags_small = json.load(dsf)

with open(dogtags_big_file) as dbf:
    dogtags_big = json.load(dbf)
#%%
def print_nicely(data):
    for d in data:
        url_1 = d[0].replace("dbkwik.webdatacommons.org/", "").replace("property/", "").replace("resource/", "")
        url_2 = d[1].replace("dbkwik.webdatacommons.org/", "").replace("property/", "").replace("resource/", "")
        print(quote(url_1, safe=":/"))
        print(dogtags_small[d[0]])
        print(quote(url_2, safe=":/"))
        print(dogtags_big[d[1]])
        print()
#%%
method_1_str = method_1_file.split("/")[-2]
method_2_str = method_2_file.split("/")[-2]

print("##### STATS #####")

print("Gold pairs count:", len(gold_pairs))
print(method_1_str, "count:", len(method_1))
print(method_2_str, "count:", len(method_2))

print("##### COMPARISON #####")

golds_that_both_find = []
for item in gold_pairs:
    if item in method_1 and item in method_2:
        golds_that_both_find.append(item)
print("Golds that both find:", len(golds_that_both_find))

golds_that_only_1_find = []
for item in gold_pairs:
    if item in method_1 and item not in method_2:
        golds_that_only_1_find.append(item)
print("Golds that only", method_1_str, "finds:", len(golds_that_only_1_find))

golds_that_only_2_find = []
for item in gold_pairs:
    if item not in method_1 and item in method_2:
        golds_that_only_2_find.append(item)
print("Golds that only", method_2_str, "finds:", len(golds_that_only_2_find))

golds_that_none_find = []
for item in gold_pairs:
    if item not in method_1 and item not in method_2:
        golds_that_none_find.append(item)
print("Golds that none find:", len(golds_that_none_find))
#%%
print("##### GOLDS THAT BOTH FIND #####\n")
print_nicely(golds_that_both_find)
#%%
print("##### GOLDS THAT NONE FIND #####\n")
print_nicely(golds_that_none_find)
#%%
print("##### GOLDS THAT ONLY", method_1_str, "FIND #####\n")

for item in golds_that_only_1_find:
    print(method_1_str, "found")
    print_nicely([item])
    found_something = False
    for i in method_2:
        if item[0] == i[0]:
            print(method_2_str, "found instead")
            print_nicely([i])
            found_something = True
    if not found_something:
        print(method_2_str, "didn't find anything\n")
    print("##################################################")
#%%
print("##### GOLDS THAT ONLY", method_2_str, "FIND #####\n")

for item in golds_that_only_2_find:
    print(method_2_str, "found")
    print_nicely([item])
    found_something = False
    for i in method_1:
        if item[0] == i[0]:
            print(method_1_str, "found instead")
            print_nicely([i])
            found_something = True
    if not found_something:
        print(method_1_str, "didn't find anything\n")
    print("##################################################\n")
#%%
