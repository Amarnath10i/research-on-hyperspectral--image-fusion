import glob
import os

print("Applying final path patches directly to file text...")
notebooks = glob.glob(r'd:\academic\project1\notebooks\**\*.ipynb', recursive=True)
patched_count = 0

for nb_file in notebooks:
    with open(nb_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace all bad prefixes globally in the raw JSON
    content = content.replace('/kaggle/input/datasets/nikeshreddypatlolla/', '/kaggle/input/')
    content = content.replace('/kaggle/input/models/nikeshreddypatlolla/', '/kaggle/input/')
    content = content.replace('/kaggle/input/nikeshreddypatlolla/', '/kaggle/input/')
    
    # Also handle the mask3d fix for ifcasformer
    if 'ifcasformer' in nb_file.lower():
        # Specifically target the pip install mask3d line
        content = content.replace('!pip install mask3d', '!pip install mask3d --no-binary :all:')
    
    if content != original_content:
        with open(nb_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {os.path.basename(nb_file)}")
        patched_count += 1

print(f"\nDone! Successfully patched {patched_count} notebooks.")
