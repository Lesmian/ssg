import os
import shutil
from markdown import markdown_to_html_node
from textnode import *

def main():
    copy_source_to_destination("static", "public")
    generate_page("content/index.md", "./template.html", "public/index.html")

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_file = open(dest_path, mode="w")
    dest_file.write(result)
    dest_file.close()

main()