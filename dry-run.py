import subprocess
import os
import toml

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

if __name__ == "__main__":
    for subject in subjects:
        run(subject)

