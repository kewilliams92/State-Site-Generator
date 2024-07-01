import os
import pathlib

from block_markdown import markdown_to_htmlnode


def generate_page(from_path, template_path, dest_path):
    print(f"Generating {from_path} {template_path} to {dest_path}...")
    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_htmlnode(markdown)
    html = node.to_html()

    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


# Generate page recursively
def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating pages from {dir_path_content} {template_path} to {dest_dir_path}..."
    )
    # List all files in the content directory
    files = os.listdir(dir_path_content)
    # using pathlib.Path to join the path
    for file in files:
        file_path = pathlib.Path(dir_path_content) / file
        if os.path.isfile(file_path):
            if file.endswith(".md"):
                dest_path = pathlib.Path(dest_dir_path) / (file[:-3] + ".html")
                generate_page(file_path, template_path, dest_path)
        elif os.path.isdir(file_path):
            dest_dir = pathlib.Path(dest_dir_path) / file
            generate_page_recursively(file_path, template_path, dest_dir)


def extract_title(markdown):
    # All pages need a single h1 header, if no header is provided: raise exception
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown content")
