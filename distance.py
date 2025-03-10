import os
import subprocess
from typing import Dict

import sbsv
import json
import matplotlib.pyplot as plt
from matplotlib import ticker
from sklearn import manifold
import numpy as np

def plot_3d(points, points_color, subject, version):
    x, y, z = points.T

    fig, ax = plt.subplots(
        figsize=(6, 6),
        facecolor="white",
        tight_layout=True,
        subplot_kw={"projection": "3d"},
    )
    fig.suptitle(f'{subject}-{version}', size=16)
    col = ax.scatter(x, y, z, c=points_color, alpha=0.8)
    ax.view_init(azim=-60, elev=9)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(1))

    fig.colorbar(col, ax=ax, orientation="horizontal", shrink=0.6, aspect=60, pad=0.01)
    if not os.path.exists('plots'):
        os.mkdir('plots')
    if not os.path.exists(f'plots/{subject}'):
        os.mkdir(f'plots/{subject}')
    plt.savefig(f'plots/{subject}/{version}.pdf')

def plot_2d(points, points_color, subject, version):
    fig, ax = plt.subplots(figsize=(3, 3), facecolor="white", constrained_layout=True)
    fig.suptitle(f'{subject}-{version}', size=16)
    add_2d_scatter(ax, points, points_color)
    if not os.path.exists('plots'):
        os.mkdir('plots')
    if not os.path.exists(f'plots/{subject}'):
        os.mkdir(f'plots/{subject}')
    plt.savefig(f'plots/{subject}/{version}.pdf')

def add_2d_scatter(ax:plt.Axes, points, points_color, title=None):
    x, y = points.T
    ax.scatter(x, y, c=points_color, alpha=0.8)
    ax.set_title(title)
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.yaxis.set_major_formatter(ticker.NullFormatter())

def parse_data():
    subject_data:Dict[str,dict]=dict() # subject: {version: data_dict}
    for path, dirnames, filenames in os.walk('new-seeds-log'):
        for file in filenames:
            if file.endswith('.gz'):
                res=subprocess.run(f'gunzip {file}',shell=True,cwd=path)
                if res.returncode!=0:
                    raise RuntimeError(f'gunzip failed for {file}')
                file=file.removesuffix('.gz')

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
                for d in branch_cov_str:
                    branch_cov.append(int(d))
                # _i=0
                # while _i!=-1:
                #     _i=branch_cov_str.find('1',_i)
                #     if _i==-1:
                #         break
                #     branch_cov.append(_i)
                #     _i+=1
                data_dict[val['file']]={
                    'target_reached':target_reached,
                    'dfg':dfg,
                    'branch_cov':branch_cov
                }

            subject_data[subject][version]=data_dict

    with open('data.json','w') as f:
        json.dump(subject_data,f)
    
    return subject_data

if os.path.exists('data.json'):
    with open('data.json') as f:
        subject_data=json.load(f)
else:
    subject_data=parse_data()

for sub in subject_data:
    for ver in subject_data[sub]:
        print(f'{sub}-{ver}')
        t_sne=manifold.TSNE(n_components=2,perplexity=30,random_state=0)
        # t_sne=manifold.TSNE(n_components=3,perplexity=30,random_state=0)
        points=[]
        points_color=[]
        for patch in subject_data[sub][ver]:
            branch_cov=subject_data[sub][ver][patch]['branch_cov']
            points.append(branch_cov)
            points_color.append(1 if subject_data[sub][ver][patch]['target_reached'] else 0)
        points=t_sne.fit_transform(np.array(points))
        plot_2d(points,points_color,sub,ver)
        # plot_3d(points,points_color,sub,ver)