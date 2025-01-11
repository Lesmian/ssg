import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n")
    blocks = filter(lambda x: x != "", blocks)
    return list(map(lambda x: x.strip(), blocks))

def block_to_block_type(block):
    if re.match(r"^#{1,6} .+", block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if len(block.split("\n")) == len(re.findall(r"^>.*", block, re.RegexFlag.M)):
        return "quote"
    if len(block.split("\n")) == len(re.findall(r"^[*-] .*", block, re.RegexFlag.M)):
        return "unordered_list"
    if is_ordered_list(block):
        return "ordered_list"
    
    return "paragraph"


def is_ordered_list(block):
    lines = block.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}."):
            return False
        
    return True