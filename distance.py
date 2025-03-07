import os
import subprocess
from typing import Dict

import sbsv
import json

subject_data:Dict[str,dict]=dict() # subject: {version: data_dict}
for path, dirnames, filenames in os.walk('new-seeds-log'):
    for file in filenames:
        if file.endswith('.gz'):
            res=subprocess.run(f'gunzip {file}',shell=True,cwd=path)
            if res.returncode!=0:
                raise RuntimeError(f'gunzip failed for {file}')

        subject=path.split('/')[-1]
        version=file.split('.')[0]
        if subject not in subject_data:
            subject_data[subject]=dict()
        print(f'{subject}-{version}')

        parser=sbsv.parser()
        parser.add_schema("[seed] [file: str] [hash: int] [dfg: int] [res: int] [time: int] [target: int] [vec: str] [trace: str]")
        with open(os.path.join(path,file)) as f:
            parser.load(f)

        data_dict:Dict[str,dict]=dict()  # patch_file: {target_reached: , dfg: list, branch_cov: list}
        for val in parser.get_result_in_order(["[seed]"]):
            target_reached=val['target']==1
            dfg=[]
            for v in val['vec'].split(','):
                if v!='':
                    dfg.append(int(v))

            branch_cov_str:str=val['trace']
            branch_cov=[]
            _i=0
            while _i!=-1:
                _i=branch_cov_str.find('1',_i)
                branch_cov.append(_i)
                _i+=1
            data_dict[val['file']]={
                'target_reached':target_reached,
                'dfg':dfg,
                'branch_cov':branch_cov
            }

        subject_data[subject][version]=data_dict

with open('data.json','w') as f:
    json.dump(subject_data,f)