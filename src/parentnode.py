from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a tag")
        
        if self.children == None:
            raise ValueError("Parent node must have children")
        
        content = "".join(map(str, self.children))
        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"