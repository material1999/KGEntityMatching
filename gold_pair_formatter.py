#%%
big = "starwars"
small = "swtor"

with open("_input/gold_pairs/" + big + "-" + small + ".txt", "r") as f:
    data = f.readlines()

with open("_input/gold_pairs/_" + small + "-" + big + ".txt", "w") as f:
    for item in data:
        item_0 = item.strip().split(";")[0]
        item_1 = item.strip().split(";")[1]
        f.write(item_1 + ";" + item_0 + "\n")

print("ID replacement completed and saved to '" + small + "-" + big + ".txt'")
#%%
