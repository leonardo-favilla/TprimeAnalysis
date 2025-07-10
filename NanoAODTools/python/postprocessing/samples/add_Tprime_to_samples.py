import json

samples_dict_path_1 = "dict_samples_2022.json"
samples_dict_path_2 = "dict_samples_2023.json"

with open(samples_dict_path_1, 'r') as file:
    samples_dict_1 = json.load(file)
with open(samples_dict_path_2, 'r') as file:
    samples_dict_2 = json.load(file)



for key in samples_dict_1:
    if ("Tprime" in key) and (key not in samples_dict_2):
        for subkey in samples_dict_1[key]:
            if key not in samples_dict_2:
                newkey              = key.replace("2022", "2023").replace("EE", "postBPix")
                newsubkey           = subkey.replace("2022", "2023").replace("EE", "postBPix")
                samples_dict_2[newkey] = {}
                samples_dict_2[newkey][newsubkey] = samples_dict_1[key][subkey]


with open(samples_dict_path_2, 'w') as file:
    json.dump(samples_dict_2, file, indent=4)
print(f"Updated {samples_dict_path_2} with Tprime samples from {samples_dict_path_1}.")