import os

seed_dirs = ["elf", "jpeg", "mp3", "xml", "html", "tiff"]
for seed_dir in seed_dirs:
    if not os.path.exists(seed_dir):
        os.makedirs(seed_dir)
    files = os.listdir(seed_dir)
    for file in files:
        filename = os.path.join(seed_dir, file)
        # If file size > 50kb, remove it
        if os.path.getsize(filename) > 50000:
            print('Removing', filename)
            os.remove(filename)