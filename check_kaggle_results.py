import os
import json
import subprocess
import sys

# PYTHONUTF8 must be set BEFORE the Python interpreter starts to take effect.
if os.environ.get("PYTHONUTF8") != "1":
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run([sys.executable, __file__], env=env)
    sys.exit(result.returncode)

def check_kaggle_status():
    print("\n--- Kaggle API Authentication ---")
    # Use legacy kaggle.json (preferred — has full API access)
    kaggle_json = os.path.join(os.path.expanduser("~"), ".kaggle", "kaggle.json")
    if os.path.exists(kaggle_json):
        with open(kaggle_json, "r") as f:
            creds = json.load(f)
        os.environ["KAGGLE_USERNAME"] = creds["username"]
        os.environ["KAGGLE_KEY"] = creds["key"]
        print(f"Using kaggle.json (username: {creds['username']})")
    else:
        # Fall back to KAGGLE_API_TOKEN env var
        token_full = os.environ.get("KAGGLE_API_TOKEN", "")
        if not token_full:
            print("✗ ERROR: No kaggle.json and no KAGGLE_API_TOKEN found.")
            return
        if "_" in token_full:
            token = token_full.split('_', 1)[1]
        else:
            token = token_full
        os.environ["KAGGLE_USERNAME"] = "amarnath10chinu"
        os.environ["KAGGLE_KEY"] = token
        print(f"Using KAGGLE_API_TOKEN (token: {token_full[:10]}...)")
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "kaggle"], check=False)
        from kaggle.api.kaggle_api_extended import KaggleApi
    
    api = KaggleApi()
    api.authenticate()
    
    username = os.environ.get("KAGGLE_USERNAME", "amarnath10chinu")
    
    # The notebooks we pushed (known slugs)
    known_slugs = [
        "amgsgan-test-cave-1",
        "dbin-test-cave-1",
        "dhifnet-test-cave",
        "fusformer-test-cave",
        "ifcasformer-test-cave-1",
        "lru-test-cave-1",
        "mogdcn-test-cave-1",
        "psrt-test-cave-1",
        "tsfn-test-cave-422233",
        "utal-test-cave-1",
        "amgsgan-test-harvard",
        "dbin-test-harvard",
        "dhifnet-test-harvard",
        "fusformer-test-harvard",
        "ifcasformer-test-harvard",
        "lru-test-harvard",
        "mogdcn-test-harvard-2",
        "psrt-test-harvard",
        "tsfn-test-harvard",
        "utal-test-harvard-1",
    ]
    
    # First try listing user's kernels
    print(f"Fetching notebooks for {username}...")
    try:
        kernels = api.kernels_list(user=username, page_size=100)
        print(f"Found {len(kernels)} notebooks via kernels_list.")
    except Exception as e:
        print(f"Warning: kernels_list failed: {e}")
        kernels = []

    results = []
    has_errors = False
    
    print("\n--- Notebook Status ---")
    
    for k in kernels:
        # A kernel object usually has attributes like 'title', 'ref', 'status'
        title = getattr(k, 'title', str(k))
        ref = getattr(k, 'ref', None)
        
        if not ref:
            continue
            
        try:
            status_response = api.kernels_status(ref)
            # status_response may be a dict or an object; handle both
            if hasattr(status_response, 'status'):
                status_raw = str(status_response.status).lower()
            elif isinstance(status_response, dict):
                status_raw = str(status_response.get('status', 'unknown')).lower()
            else:
                status_raw = str(status_response).lower()
            
            # Format the status nicely
            display_status = status_raw.replace("kernelworkerstatus.", "")
            
            print(f"[{display_status.upper():12s}] {ref} (Title: {title})")
            results.append({"ref": ref, "title": title, "status": display_status})
            
            # If a notebook failed, download its output log for analysis
            if display_status in ("error", "cancelacknowledged", "failed"):
                has_errors = True
                print(f"  -> Downloading error log for {ref}...")
                slug = ref.split("/")[-1] if "/" in ref else ref
                log_dir = os.path.join(r"d:\academic\project1", "kaggle_logs", slug)
                os.makedirs(log_dir, exist_ok=True)
                try:
                    api.kernels_output(ref, path=log_dir)
                    print(f"  -> Log saved to kaggle_logs/{slug}/")
                except Exception as log_err:
                    print(f"  -> Could not download log: {log_err}")
        except Exception as e:
            print(f"[ERROR       ] {ref}: {e}")
            results.append({"ref": ref, "status": "check_failed", "error": str(e)})

    # Save summary
    summary_path = r"d:\academic\project1\kaggle_status_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nStatus summary saved to {summary_path}")
    if has_errors:
        print("Some notebooks had errors. Logs downloaded to the 'kaggle_logs' directory.")
    else:
        print("No errors detected so far! (Notebooks may still be running — recheck in a few minutes.)")

if __name__ == "__main__":
    check_kaggle_status()
