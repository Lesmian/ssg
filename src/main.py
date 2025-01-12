import os
import shutil
from leafnode import LeafNode
from textnode import *
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link

def main():
    copy_source_to_destination("static", "public")

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type")
        
def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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