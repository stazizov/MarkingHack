import numpy as np
import json
import os
import pandas as pd

with open("interface.json") as f:
    config = json.load(f)

with open(os.path.join(config["download_folder"], config["inn_2_coords_filename"])) as f:
    final = json.load(f)

with open(os.path.join(config["download_folder"], config["sender_receiver_filename"])) as f:
    sender_receiver = json.load(f)

copy = dict()

for k, v in sender_receiver.items():
    copy[k] = list(np.unique(v))

sender_receiver = copy


def find_sequence(sender, hashmap, keys, threshold, i=0):
    if i == threshold:
        return []
    
    if sender not in keys:
        return []
    
    sequence = []

    sequence.append(sender)

    for rec in hashmap[sender]:
        sequence.append(rec)

        if rec not in keys:
            return sequence
        
        return sequence + find_sequence(rec, hashmap, keys, threshold, i + 1)


def seq_to_coords(sequence, hashmap, keys):
    ans = []

    for inn in sequence:
        if inn not in keys:
            if len(ans) < 2:
                return []
            return ans
        ans.append(hashmap[inn])


def create_supply_chains(inn: str, lower_threshold: int = 2, upper_threshold: int = 20):
    if inn:
        hashmap = {k: v for k, v in sender_receiver.items() if k == inn}
    else:
        hashmap = {k: v for k, v in sender_receiver.items()}
    sequences = []

    for k in sender_receiver.keys():
        tmp = find_sequence(k, hashmap, hashmap.keys(), upper_threshold)
        tmp = seq_to_coords(tmp, final, final.keys())
        if bool(tmp):
            sequences.append(tmp)
    
    sequences = list(filter(lambda x: len(x) >= lower_threshold, sequences))
    sequences = [item for sublist in sequences for item in sublist]

    test = sequences
    if len(sequences) > 200:
        test = sequences[:100] + sequences[-100:]
    
    test_dict = {
    "lon": [],
    "lat": [],
    "lon2": [],
    "lat2": []
    }

    for i in range(1, len(test)):
        lat, lon = test[i - 1]
        lat2, lon2 = test[i]

        test_dict["lon2"].append(lon2)
        test_dict["lat2"].append(lat2)
        test_dict["lon"].append(lon)
        test_dict["lat"].append(lat)

    return pd.DataFrame(test_dict)