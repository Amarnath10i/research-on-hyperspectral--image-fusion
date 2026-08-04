import json
with open(r'd:\academic\project1\notebooks\cave\mogdcn-test-cave (1).ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        for line in cell['source']:
            if 'DATA_ROOT' in line or 'CKPT_PATH' in line or 'mask3d' in line:
                print(repr(line))
