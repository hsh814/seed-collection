from typing import Dict, List

import numpy as np
import scipy
import os
import sys

magma_seeds:Dict[str,List[np.ndarray]]=dict()

subject=sys.argv[1]

# Read magma seeds
for path, directories, files in os.walk(f'seeds/{subject}'):
    for file in files:
        rel_path=path.removeprefix(f'seeds/{subject}/')
        if len(rel_path) <= 1:
            # A root path
            continue

        if rel_path not in magma_seeds:
            magma_seeds[rel_path]=[]
        with open(os.path.join(path,file),'rb') as f:
            data=f.read()
            magma_seeds[rel_path].append(np.frombuffer(data,dtype=np.int8))

for path, dirs, files in os.walk(f'magma-seeds/{subject}'):
    for file in files:
        rel_path = path.removeprefix(f'magma-seeds/{subject}/')
        if len(rel_path) <= 1:
            # A root path
            continue

        with open(os.path.join(path, file), 'rb') as f:
            data=f.read()

        data_array=np.frombuffer(data,dtype=np.int8)
        dists=[]
        for base in magma_seeds:
            for base_data in magma_seeds[base]:
                if len(data_array) > len(base_data):
                    base_data=np.pad(base_data,(0,len(data_array)-len(base_data)),constant_values=(0,0))
                else:
                    data_array=np.pad(data_array,(0,len(base_data)-len(data_array)),constant_values=(0,0))
                dist=scipy.spatial.distance.hamming(data_array,base_data)
                dists.append(dist)

        print(f'{os.path.join(path,file)}: mean: {np.mean(dists)}, median: {np.median(dists)}, len: {len(dists)}')