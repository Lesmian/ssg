import os
import shutil
from leafnode import LeafNode
from textnode import *
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link

def main():
    copy_source_to_destination("static", "public")

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

main()