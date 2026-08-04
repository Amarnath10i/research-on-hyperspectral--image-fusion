import os
import shutil
import subprocess
import json
import sys

# Force UTF-8 encoding for all Python file operations (fixes the charmap error in Kaggle CLI)
os.environ["PYTHONUTF8"] = "1"

# ==========================================
# 1. ORGANIZE DIRECTORY STRUCTURE
# ==========================================
def organize_files():
    print("Organizing files into GitHub repository structure...")
    base_dir = r"d:\academic\project1"
    
    dirs = [
        "literature_survey",
        r"notebooks\cave",
        r"notebooks\harvard",
        "papers"
    ]
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    # Move literature survey files
    lit_files = [
        "lit_search.py", "check_oa.py", "lit_multimodal.py",
        "build_lit_excel.py", "create_excel.py", "create_excel_fusion.py",
        "lit_raw.json", "lit_candidates.json", "lit_multimodal.json"
    ]
    for f in lit_files:
        src = os.path.join(base_dir, f)
        if os.path.exists(src):
            shutil.move(src, os.path.join(base_dir, "literature_survey", f))

    # Move notebooks
    nb_dir = os.path.join(base_dir, "Notebooks_cave_harvard")
    if os.path.exists(nb_dir):
        for f in os.listdir(nb_dir):
            if f.endswith(".ipynb"):
                src = os.path.join(nb_dir, f)
                if "cave" in f.lower():
                    shutil.move(src, os.path.join(base_dir, "notebooks", "cave", f))
                elif "harvard" in f.lower():
                    shutil.move(src, os.path.join(base_dir, "notebooks", "harvard", f))

    # Move papers (if they are in root)
    for f in os.listdir(base_dir):
        if f.endswith(".pdf"):
            shutil.move(os.path.join(base_dir, f), os.path.join(base_dir, "papers", f))

    print("✓ Directory structure organized.")

# ==========================================
# 2. CONFIGURE KAGGLE API
# ==========================================
def configure_kaggle():
    print("\n--- Kaggle Configuration ---")
    print("Your previous attempt returned '401 Unauthorized'. This means the username and API key didn't match.")
    username = input("Enter your exact Kaggle username from your profile URL (try 'amarnath10' if 'amarnath10chinu' failed): ").strip()
    
    # The user provided token KGAT_c8889ab9939df9618e59f3e13fcea8fa
    token = "KGAT_c8889ab9939df9618e59f3e13fcea8fa"
    
    # Remove KGAT_ if present for traditional kaggle.json auth
    key = token.replace("KGAT_", "")
    
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    
    creds = {
        "username": username,
        "key": key
    }
    
    cred_file = os.path.join(kaggle_dir, "kaggle.json")
    with open(cred_file, "w") as f:
        json.dump(creds, f)
    
    if os.name != 'nt':
        os.chmod(cred_file, 0o600)
        
    print(f"✓ Kaggle credentials saved to {cred_file}")
    
    # Some new Kaggle environments prefer environment variables instead of kaggle.json
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_KEY"] = key
    
    return username

# ==========================================
# 3. PUSH NOTEBOOKS TO KAGGLE
# ==========================================
def push_notebooks(username):
    print("\n--- Pushing Notebooks to Kaggle ---")
    base_dir = r"d:\academic\project1"
    
    print("Installing Kaggle CLI if not present...")
    subprocess.run(["pip", "install", "kaggle"], check=False)
    
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    notebooks = []
    cave_dir = os.path.join(base_dir, "notebooks", "cave")
    harvard_dir = os.path.join(base_dir, "notebooks", "harvard")
    
    if os.path.exists(cave_dir):
        notebooks.extend([(cave_dir, f) for f in os.listdir(cave_dir) if f.endswith(".ipynb")])
    if os.path.exists(harvard_dir):
        notebooks.extend([(harvard_dir, f) for f in os.listdir(harvard_dir) if f.endswith(".ipynb")])
        
    print(f"Found {len(notebooks)} notebooks to push.")
    
    for ndir, nfile in notebooks:
        print(f"\nProcessing {nfile}...")
        npath = os.path.join(ndir, nfile)
        
        with open(npath, "r", encoding="utf-8") as f:
            nb_content = json.load(f)
            
        dataset_sources = []
        model_sources = []
        
        # Link datasets and models based on the notebook name
        if "cave" in nfile.lower():
            dataset_sources.append("nikeshreddypatlolla/cave-dataset-2")
        elif "harvard" in nfile.lower():
            dataset_sources.append("nikeshreddypatlolla/harvard-hsi-2")
            
        if "fusformer" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-fusformer/frameworks/pytorch")
        elif "tsfn" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-tsfn-epoch500/frameworks/tensorflow2")
        elif "ifcasformer" in nfile.lower():
            dataset_sources = ["nikeshreddypatlolla/cave-dataset-3", "nikeshreddypatlolla/casformer-mask"]
            model_sources.append("nikeshreddypatlolla/ifcasformer/frameworks/pytorch")
        elif "amgsgan" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/amgsgan-model/frameworks/pytorch")
        elif "dbin" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-sf16-15k/frameworks/tensorflow2")
        elif "dhifnet" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-dhifnet/frameworks/pytorch")
        elif "lru" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-lru/frameworks/pytorch")
        elif "mogdcn" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-mogdcn/frameworks/pytorch")
        elif "psrt" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-psrt/frameworks/pytorch")
        elif "utal" in nfile.lower():
            model_sources.append("nikeshreddypatlolla/model-utal/frameworks/pytorch")

        # Create kernel-metadata.json
        slug = nfile.replace(".ipynb", "").replace(" ", "-").replace("(", "").replace(")", "").lower()
        meta = {
            "id": f"{username}/{slug}",
            "title": slug,
            "code_file": nfile,
            "language": "python",
            "kernel_type": "notebook",
            "is_private": "true",
            "enable_gpu": "true",
            "enable_internet": "true",
            "dataset_sources": dataset_sources,
            "competition_sources": [],
            "kernel_sources": [],
            "model_sources": model_sources
        }
        
        meta_path = os.path.join(ndir, "kernel-metadata.json")
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
            
        # Push to Kaggle
        print(f"Pushing {slug} to Kaggle...")
        try:
            api.kernels_push(ndir)
            print(f"✓ Successfully pushed {slug}")
        except Exception as e:
            print(f"✗ Failed to push {slug}: {e}")
            
        # Clean up metadata file
        if os.path.exists(meta_path):
            os.remove(meta_path)

if __name__ == "__main__":
    organize_files()
    username = configure_kaggle()
    push_notebooks(username)
    print("\nAll tasks completed! You can check the execution status at: https://www.kaggle.com/" + username)
