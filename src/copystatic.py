import os
import shutil


def copy_files_recursive(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        print(f"Creating {destination_dir}...")
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        print(f"Processing {filename}")
        from_path = os.path.join(source_dir, filename)
        to_path = os.path.join(destination_dir, filename)
        print(f"Copying {from_path} to {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_files_recursive(from_path, to_path)
