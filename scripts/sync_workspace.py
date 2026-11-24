import os
import shutil

src_root = os.path.abspath(".")
dst_root = os.path.abspath(r"C:\Users\PAUL\Documents\Projects\VitalSphere")

print(f"Syncing from {src_root} to {dst_root}...")

items_to_sync = [
    "public",
    "src",
    "firebase.json",
    "scripts",
    "pom.xml",
    "Report and PPT"
]

for item in items_to_sync:
    s_path = os.path.join(src_root, item)
    d_path = os.path.join(dst_root, item)
    if os.path.isdir(s_path):
        if os.path.exists(d_path):
            shutil.rmtree(d_path)
        shutil.copytree(s_path, d_path)
        print(f"Synced dir {item}")
    elif os.path.isfile(s_path):
        shutil.copy2(s_path, d_path)
        print(f"Synced file {item}")

print("Sync completed successfully.")
