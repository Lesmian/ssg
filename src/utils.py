from leafnode import LeafNode
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and delimiter in node.text:
            new_nodes.extend(split_node(node.text, delimiter, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
    
def split_node(text, delimiter, text_type):
    text_parts = text.split(delimiter, 2)
    if len(text_parts) < 3:
        print(text_parts)
        raise Exception("Invalid markdown")
    
    result = []
    if text_parts[0] != "":
        result.append(TextNode(text_parts[0], TextType.TEXT))
    result.append(TextNode(text_parts[1], text_type))
    if delimiter in text_parts[2]:
        result.extend(split_node(text_parts[2], delimiter, text_type))
    elif text_parts[2] != '':
        result.append(TextNode(text_parts[2], TextType.TEXT))
    
    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            input_text = node.text
            for img in images:
                markdown = f"![{img[0]}]({img[1]})"
                (nodes, new_Text) = split_node_markdown(img, input_text, markdown, TextType.IMAGE)
                new_nodes.extend(nodes)
                input_text = new_Text
            if len(input_text) > 0:
                new_nodes.append(TextNode(input_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            input_text = node.text
            for link in links:
                markdown = f"[{link[0]}]({link[1]})"
                (nodes, new_Text) = split_node_markdown(link, input_text, markdown, TextType.LINK)
                new_nodes.extend(nodes)
                input_text = new_Text
            if len(input_text) > 0:
                new_nodes.append(TextNode(input_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_node_markdown(img, text, markdown, type):
    nodes = []
    index = text.find(markdown)
    if index > 0:
        nodes.append(TextNode(text[:index], TextType.TEXT))
    nodes.append(TextNode(img[0], type, img[1]))
    return nodes, text[index + len(markdown):]

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.+?)\)", text)

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
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes