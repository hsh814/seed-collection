import os

seed_dirs = ["elf", "jpeg", "mp3", "xml", "html", "tiff"]
for seed_dir in seed_dirs:
    if not os.path.exists(os.path.join("new-seeds", seed_dir)):
        continue
        os.makedirs(seed_dir)
    files = os.listdir(os.path.join("new-seeds", seed_dir))
    for file in files:
        filename = os.path.join("new-seeds", seed_dir, file)
        # If file size > 100kb, remove it
        if os.path.getsize(filename) > 100000:
            print('Removing', filename)
            os.remove(filename)