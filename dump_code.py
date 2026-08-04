import json
import glob
import os

for nb_file in glob.glob(r'd:\academic\project1\notebooks\cave\*.ipynb'):
    name = os.path.basename(nb_file)
    if 'mogdcn' in name or 'amgsgan' in name or 'ifcasformer' in name:
        with open(nb_file, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        with open(nb_file + '.py', 'w', encoding='utf-8') as out:
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    out.write(''.join(cell['source']) + '\n\n')
