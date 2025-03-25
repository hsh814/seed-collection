import os
import shutil
import sys
from typing import List, Set, Tuple
import requests
import json

TOTAL_TRIAL=10
ANSWER_ONCE=50

if os.path.exists('coreutils-seeds'):
    shutil.rmtree('coreutils-seeds')
os.mkdir('coreutils-seeds')

for f in os.listdir('coreutils-help'):
    print(f'Processing {f}...')
    result:Set[Tuple[str]]=set()
    with open(f'coreutils-help/{f}','r') as file:
        text=file.read()

    user_msg=f"""
You will get a help message of a program. Please generate various lists of arguments and options to test a target program based on the given help message.

Please follow the rules below:

1. Give me lists of arguments and options only. Do NOT give any description.
2. Give me the {ANSWER_ONCE} answers in JSON format. Put arguments and options in a single json array. Give me a json array of {ANSWER_ONCE} arrays.
3. It should NOT throw any parsing error.

```
{text}
```
"""

    data={"model":"gpt-3.5-turbo",
        "messages":[{
                "role":"developer",
                "content":"You are the best software tester."
            },
            {
                "role":"user",
                "content":f"{user_msg}"
            }
        ]
    }
    # print(data)

    for i in range(TOTAL_TRIAL):
        print(f'Trial {i+1}/{TOTAL_TRIAL}...')
        req=requests.post('https://api.openai.com/v1/chat/completions',headers={
            'Content-Type':'application/json',
            'Authorization':f'Bearer {os.getenv("OPENAI_API_KEY")}'
        },data=json.dumps(data))
        res=req.json()
        res_output=res['choices'][0]['message']['content'].replace('```\n','').replace('\n```','')
        # print(f'New input is generated:\n{res_output}')

        res_output=res_output.removeprefix('```json\n').removesuffix('```')
        try:
            r=json.loads(res_output)
        except json.JSONDecodeError:
            print(f'Error in parsing JSON. Retry.')
            i-=1
            continue
        for a in r:
            if len(a)>0:
                result.add(tuple(a))

    os.mkdir(f'coreutils-seeds/{f}')
    for i,answer in enumerate(result):
        with open(f'coreutils-seeds/{f}/{i}.txt','w') as file:
            file.write(' '.join(answer))
    print(f'{f} is done.')