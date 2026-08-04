import os
import subprocess

print("--- GitHub Push Setup ---")
username = input("Enter your exact GitHub username: ").strip()
repo_name = "hyperspectral-image-fusion"

print("\nRemoving old origin...")
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)

remote_url = f"https://github.com/{username}/{repo_name}.git"
print(f"Adding new origin: {remote_url}")
subprocess.run(["git", "remote", "add", "origin", remote_url])

print("\nApplying network fixes to prevent timeout errors...")
subprocess.run(["git", "config", "--global", "http.postBuffer", "524288000"])
subprocess.run(["git", "config", "--global", "http.version", "HTTP/1.1"])

print("Pushing to GitHub (this may take a minute depending on your connection)...")
result = subprocess.run(["git", "push", "-u", "origin", "main"])

if result.returncode == 0:
    print("\n✓ Successfully pushed to GitHub!")
else:
    print("\n✗ Failed to push. Make sure your GitHub username is correct and you have access.")
