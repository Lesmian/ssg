import os
import pathlib
import shutil
import sys
from markdown import markdown_to_html_node
from textnode import *

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]


    copy_source_to_destination("static", "docs")
    generate_pages_recursive(basepath, "./content", "./template.html", "./docs")

def copy_source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)
    paths = os.listdir(source)
    for path in paths:
        sourcePath = os.path.join(source, path)
        destinationPath = os.path.join(destination, path)
        if os.path.isfile(sourcePath):
            shutil.copy(sourcePath, destinationPath)
        else:
            copy_source_to_destination(sourcePath, destinationPath)

def extract_title(markdown):
    lines = markdown.split("\n")
    if len(lines) == 0 or not lines[0].startswith("# "):
        raise Exception("Markdown doesn't contain title")
    
    return lines[0][1:].strip()

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html)
    result = result.replace('href="/', f'href="{basepath}')
    result = result.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_file = open(dest_path, mode="w")
    dest_file.write(result)
    dest_file.close()

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    paths = os.listdir(dir_path_content)
    for path in paths:
        sourcePath = os.path.join(dir_path_content, path)
        filename = pathlib.Path(sourcePath).stem
        ext = pathlib.Path(sourcePath).suffix
        is_file = os.path.isfile(sourcePath)
        if is_file and ext == ".md":
            destinationPath = os.path.join(dest_dir_path, filename + ".html")
            generate_page(basepath, sourcePath, template_path, destinationPath)
        elif not is_file:
            destinationPath = os.path.join(dest_dir_path, path)
            generate_pages_recursive(basepath, sourcePath, template_path, destinationPath)

main()