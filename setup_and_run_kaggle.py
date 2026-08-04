import os
import shutil
import subprocess
import json
import sys

# PYTHONUTF8 must be set BEFORE the Python interpreter starts to take effect.
# If it wasn't set, re-launch this script with it in the environment.
if os.environ.get("PYTHONUTF8") != "1":
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run([sys.executable, __file__], env=env)
    sys.exit(result.returncode)

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
    
    # Prefer legacy kaggle.json (full API access)
    kaggle_json = os.path.join(os.path.expanduser("~"), ".kaggle", "kaggle.json")
    if os.path.exists(kaggle_json):
        with open(kaggle_json, "r") as f:
            creds = json.load(f)
        username = creds["username"]
        os.environ["KAGGLE_USERNAME"] = username
        os.environ["KAGGLE_KEY"] = creds["key"]
        print(f"✓ Kaggle authentication configured via kaggle.json (username: {username})")
        return username
    
    # Fall back to KAGGLE_API_TOKEN env var
    username = "amarnath10chinu"
    token_full = os.environ.get("KAGGLE_API_TOKEN", "")
    if not token_full:
        print("✗ ERROR: No kaggle.json and no KAGGLE_API_TOKEN found.")
        sys.exit(1)
    
    if "_" in token_full:
        token = token_full.split('_', 1)[1]
    else:
        token = token_full
    
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_KEY"] = token
    
    print(f"✓ Kaggle authentication configured (token: {token_full[:10]}...)")
    return username

# ==========================================
# 3. PUSH NOTEBOOKS TO KAGGLE
# ==========================================
def push_notebooks(username):
    print("\n--- Pushing Notebooks to Kaggle ---")
    base_dir = r"d:\academic\project1"
    
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
    
    success_count = 0
    fail_count = 0
    
    for ndir, nfile in notebooks:
        print(f"\nProcessing {nfile}...")
        npath = os.path.join(ndir, nfile)
            
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

        # Create a clean slug from the filename
        slug = nfile.replace(".ipynb", "").replace(" ", "-").replace("(", "").replace(")", "").lower()
        
        # Use a temporary directory so the Kaggle API only sees ONE notebook
        tmp_dir = os.path.join(base_dir, "_kaggle_tmp")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
        
        # Copy the notebook into the temp dir
        shutil.copy2(npath, os.path.join(tmp_dir, nfile))
        
        # Write kernel-metadata.json into the temp dir
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
        
        meta_path = os.path.join(tmp_dir, "kernel-metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
            
        # Push to Kaggle
        print(f"Pushing {slug} to Kaggle...")
        try:
            api.kernels_push(tmp_dir)
            print(f"✓ Successfully pushed {slug}")
            success_count += 1
        except Exception as e:
            print(f"✗ Failed to push {slug}: {e}")
            fail_count += 1
            
        # Clean up temp dir
        shutil.rmtree(tmp_dir, ignore_errors=True)
    
    print(f"\n--- Summary ---")
    print(f"✓ Succeeded: {success_count}")
    print(f"✗ Failed:    {fail_count}")
    print(f"Total:       {len(notebooks)}")

if __name__ == "__main__":
    organize_files()
    username = configure_kaggle()
    push_notebooks(username)
    print("\nAll tasks completed! You can check the execution status at: https://www.kaggle.com/" + username)
