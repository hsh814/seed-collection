import subprocess
import os
import sys
from typing import Dict, List
import toml
import sbsv

import math
import numpy as np
from sklearn.cluster import KMeans

SEED_COLLECTION_DIR = "/home/yuntong/seed-collection"
VULNFIX_DIR = "/home/yuntong/vulnfix"

subjects = [
  # "binutils/cve_2017_6965",
  # "binutils/cve_2017_14745",
  # "binutils/cve_2017_15025",
  # "coreutils/gnubug_19784",
  # "coreutils/gnubug_25003",
  # "coreutils/gnubug_25023",
#   "coreutils/gnubug_26545",
#   "jasper/cve_2016_8691",
#   "jasper/cve_2016_9557",
#   "libjpeg/cve_2012_2806",
#   "libjpeg/cve_2017_15232",
#   "libming/cve_2016_9264",
  # "libtiff/bugzilla_2633",
  # "libtiff/cve_2016_5321",
  # "libtiff/cve_2016_9532",
  # "libtiff/cve_2016_10094",
  # "libtiff/cve_2017_7595",
  # "libtiff/cve_2017_7599",
  # "libtiff/cve_2017_7600",
  # "libtiff/cve_2017_7601",
  # "libxml2/cve_2012_5134",
  # "libxml2/cve_2016_1838",
  # "libxml2/cve_2016_1839",
  # "libxml2/cve_2017_5969",
  # "zziplib/cve_2017_5974",
  # "zziplib/cve_2017_5975",
  # "zziplib/cve_2017_5976"
]

def print_log(msg):
    print(msg, file=sys.stderr)

def clustering(data: List[dict]) -> List[dict]:
    x = np.array([d["branch_cov"] for d in data])
    k = max(1, int(math.sqrt(len(data) // 2)))
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, random_state=55)
    kmeans.fit(x)
    clusters = list()
    print_log(f"Clustering: {len(data)} data points into {k} clusters")
    for cluster_id in range(kmeans.n_clusters):
        mem_indices = np.where(kmeans.labels_ == cluster_id)[0]
        cluster = {
            'centroid': kmeans.cluster_centers_[cluster_id].tolist(),
            'members': [data[i] for i in mem_indices]
        }
        clusters.append(cluster)
    return clusters

def get_rank(subject: str):
    result_file = os.path.join(VULNFIX_DIR, "data", subject, "cludafl_out", "out-dry-run", "dry_run_results.sbsv")
    parser=sbsv.parser()
    parser.add_schema("[seed] [file: str] [hash: int] [dfg: int] [res: int] [time: int] [target: int] [vec: str] [trace: str]")
    with open(result_file) as f:
        parser.load(f)

    target_reached_dict: Dict[str, dict] = dict()
    data_list: List[dict] = list() # patch_file: {target_reached: , dfg: list, branch_cov: list}
    data_dict: Dict[str, dict] = dict()  # patch_file: {target_reached: , dfg: list, branch_cov: list}
    for val in parser.get_result_in_order(["[seed]"]):
        target_reached=val['target']==1
        dfg=[]
        for v in val['vec'].split(','):
            if v!='':
                dfg.append(int(v))

        branch_cov_str:str=val['trace']
        branch_cov=[]
        for d in branch_cov_str:
            branch_cov.append(int(d))
        
        file = val['file']
        data_list.append({
            'file': val['file'],
            'target_reached':target_reached,
            'dfg':dfg,
            'dfg_score': sum(dfg),
            'branch_cov':branch_cov
        })
        data_dict[file] = data_list[-1]
        if target_reached:
            target_reached_dict[val['file']] = data_list[-1]
    
    # Clustering
    clusters = clustering(data_list)
    file_cluster_map = dict()
    cluster_scores = dict()
    for cluster_id, cluster in enumerate(clusters):
        score = 0
        for member in cluster['members']:
            file_cluster_map[member['file']] = {
                'cluster_id': cluster_id,
                'centroid': cluster['centroid'],
                'dfg_score': member['dfg_score']
            }
            score += member['dfg_score']
        cluster_scores[cluster_id] = score / len(cluster['members'])
    # Rank
    rank_data = list()
    # Priority 1: target reached
    # Priority 2: cluster's Average DAFL score (sum of dfg)
    # Priority 3: DAFL score of node (sum of dfg)
    # First, sort clusters by average DAFL score
    sorted_cluster_ids = sorted(cluster_scores.keys(), key=lambda cid: cluster_scores[cid], reverse=True)
    sorted_clusters = dict()
    print_log(f"sorted_cluster_ids: {sorted_cluster_ids}")
    for cluster_id in sorted_cluster_ids:
        # Sort members by DAFL score
        sorted_members = sorted(clusters[cluster_id]['members'], key=lambda x: x["dfg_score"], reverse=True)
        sorted_clusters[cluster_id] = sorted_members
        # Add target reached members to rank data
        for member in sorted_members:
            if member['target_reached']:
                rank_data.append(member['file'])
    # Add non-target reached members to rank data
    while len(sorted_clusters) > 0:
        remove_cluster_ids = list()
        for cluster_id, members in sorted_clusters.items():
            while True:
                target = members.pop(0)
                if not target['target_reached']:
                    rank_data.append(target['file'])
                    break
                if len(members) == 0:
                    break
            if len(members) == 0:
                remove_cluster_ids.append(cluster_id)
        for cluster_id in remove_cluster_ids:
            del sorted_clusters[cluster_id]
    # Save rank data to file
    rank_dir = os.path.join(SEED_COLLECTION_DIR, "rank", subject)
    os.makedirs(rank_dir, exist_ok=True)
    with open(os.path.join(rank_dir, "rank.csv"), "w") as f:
        for rank in rank_data:
            f.write(f"{rank}\n")

def run(subject: str):
    print(f'running {subject}')
    with open(os.path.join(SEED_COLLECTION_DIR, "vulnfix.toml")) as f:
        config = toml.load(f)
    subj, vers = subject.split("/")
    file_type = config[subj][vers]
    env = os.environ.copy()
    env["AFL_OPTS_COMMON_OVERRIDE"] = "-t 2000+ -m none -d -s dafl -r"
    env["SEED_DIR_OVERRIDE"] = os.path.join(SEED_COLLECTION_DIR, "new-seeds", file_type)
    subprocess.run(f"./run-cludafl-single.sh dry-run", shell=True, env=env, cwd=os.path.join(VULNFIX_DIR, "data", subject))
    get_rank(subject)

if __name__ == "__main__":
    for subject in subjects:
        # run(subject)
        get_rank(subject)

