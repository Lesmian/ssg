from blocks import block_to_block_type, markdown_to_blocks
import re

from parentnode import ParentNode
from utils import text_node_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))

    return ParentNode("div", children=children)

def block_to_html_node(block, block_type):
    match(block_type):
        case "paragraph":
            return ParentNode("p", children=text_to_children(block))
        case "heading":
            return block_to_heading(block)
        case "code":
            return block_to_code(block)
        case "quote":
            return block_to_quote(block)
        case "unordered_list":
            return block_to_unordered_list(block)
        case "ordered_list":
            return block_to_ordered_list(block)
        
def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def block_to_heading(block):
    match_result = re.match(r"^#{1,6}", block)
    markdown = match_result.group(0)
    heading_lvl = len(markdown)
    return ParentNode(f"h{heading_lvl}", children=text_to_children(block.lstrip(f"{markdown} ")))

def block_to_code(block):
    return ParentNode("code", children=text_to_children(block[3:-3]))

def block_to_quote(block):
    lines = block.split("\n")
    linwa = filter(lambda x: len(x) != 0, lines)
    code = " ".join(map(lambda x: x[1:].strip(), lines))
    return ParentNode("blockquote", children=text_to_children(code.strip()))

def block_to_unordered_list(block):
    lines = block.split("\n")
    children = list(map(lambda x: ParentNode("li", children=text_to_children(x[1:].strip())), lines))
    return ParentNode("ul", children=children)

def block_to_ordered_list(block):
    lines = block.split("\n")
    striped_lines = list(map(remove_ordered_list_markdown, lines))
    children = list(map(lambda x: ParentNode("li", children=text_to_children(x.strip())), striped_lines))
    return ParentNode("ol", children=children)

def remove_ordered_list_markdown(text):
    match_result = re.match(r"^\d+\.", text)
    markdown = match_result.group(0)
    return text.lstrip(markdown)