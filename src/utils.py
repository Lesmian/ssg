from textnode import TextNode, TextType

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