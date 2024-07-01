import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page_recursively

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
file_path_template = "./template.html"


def main():
    if os.path.exists(dir_path_public):
        print(f"Removing {dir_path_public} please wait...")
        shutil.rmtree(dir_path_public)

    print(f"Copying {dir_path_static} to {dir_path_public} please wait...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print(
        f"Generating page from {dir_path_content} and {file_path_template} please wait..."
    )
    generate_page_recursively(dir_path_content, file_path_template, dir_path_public)


main()
