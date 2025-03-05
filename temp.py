import os
import shutil


def get_sbsv_line(type:str, path:str, new_name:str):
    return f'[meta] [type {type}] [origin {path}] [name {new_name}]'

f=open('meta.sbsv','w')

tiff_i=0
for path, dirnames, filenames in os.walk('magma/libtiff'):
    for file in filenames:
        sbsv_string=get_sbsv_line('tiff',os.path.join(path,file).removeprefix(os.getcwd()),f'{tiff_i}.tiff')
        print(sbsv_string)
        print(sbsv_string,file=f)
        shutil.copyfile(os.path.join(path,file),f'new-seeds/tiff/{tiff_i}.tiff')
        tiff_i+=1

print()

for path, dirnames, filenames in os.walk('pass-seeds/libtiff'):
    for file in filenames:
        sbsv_string=get_sbsv_line('tiff',os.path.join(path,file).removeprefix(os.getcwd()),f'{tiff_i}.tiff')
        print(sbsv_string)
        print(sbsv_string,file=f)
        shutil.copyfile(os.path.join(path,file),f'new-seeds/tiff/{tiff_i}.tiff')
        tiff_i+=1

print()
xml_i=0
for path, dirnames, filenames in os.walk('magma/libxml2'):
    for file in filenames:
        sbsv_string=get_sbsv_line('xml',os.path.join(path,file).removeprefix(os.getcwd()),f'{xml_i}.xml')
        print(sbsv_string)
        print(sbsv_string,file=f)
        shutil.copyfile(os.path.join(path, file), f'new-seeds/xml/{xml_i}.xml')
        xml_i+=1

for path, dirnames, filenames in os.walk('pass-seeds/libxml2'):
    for file in filenames:
        sbsv_string=get_sbsv_line('xml',os.path.join(path,file).removeprefix(os.getcwd()),f'{xml_i}.xml')
        print(sbsv_string)
        print(sbsv_string,file=f)
        shutil.copyfile(os.path.join(path, file), f'new-seeds/xml/{xml_i}.xml')
        xml_i+=1

print()

html_i=0
for path, dirnames, filenames in os.walk('pass-seeds/html'):
    for file in filenames:
        sbsv_string=get_sbsv_line('html',os.path.join(path,file).removeprefix(os.getcwd()),f'{html_i}.html')
        print(sbsv_string)
        print(sbsv_string,file=f)
        shutil.copyfile(os.path.join(path, file), f'new-seeds/html/{html_i}.html')
        html_i+=1