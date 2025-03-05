from typing import Dict, List

import numpy as np
import scipy
import os
import sys
import argparse

new_seeds:Dict[str,List[np.ndarray]]=dict()

arg_parser=argparse.ArgumentParser(prog='distance.py')
arg_parser.add_argument('dir_1',action='store',type=str,help='Base seed directory')
arg_parser.add_argument('dir_2',action='store',type=str,help='Target seed directory to compare')
arg_parser.add_argument('subject',action='store',type=str,help='Target subject')
args=arg_parser.parse_args(sys.argv[1:])

subject=args.subject
dir_1=os.path.abspath(args.dir_1)
dir_2=os.path.abspath(args.dir_2)

for path, directories, files in os.walk(f'{dir_2}/{subject}'):
    for file in files:
        rel_path=path.removeprefix(f'{dir_2}/{subject}/')
        if len(rel_path) <= 1:
            # A root path
            continue

        if rel_path not in new_seeds:
            new_seeds[rel_path]=[]
        with open(os.path.join(path,file),'rb') as f:
            data=f.read()
            new_seeds[rel_path].append(np.frombuffer(data, dtype=np.int8))

for path, dirs, files in os.walk(f'{dir_1}/{subject}'):
    for file in files:
        rel_path = path.removeprefix(f'{dir_1}/{subject}/')
        if len(rel_path) <= 1:
            # A root path
            continue

        with open(os.path.join(path, file), 'rb') as f:
            data=f.read()

        data_array=np.frombuffer(data,dtype=np.int8)
        dists=[]
        for base in new_seeds:
            for base_data in new_seeds[base]:
                if len(data_array) > len(base_data):
                    base_data=np.pad(base_data,(0,len(data_array)-len(base_data)),constant_values=(0,0))
                else:
                    data_array=np.pad(data_array,(0,len(base_data)-len(data_array)),constant_values=(0,0))
                dist=scipy.spatial.distance.hamming(data_array,base_data)
                dists.append(dist)

        print(f'{os.path.join(path,file)}: mean: {np.mean(dists)}, median: {np.median(dists)}, len: {len(dists)}')