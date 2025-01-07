class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if (self.props == None):
            return ""
        
        return " " + " ".join(map(lambda tuple: f'{tuple[0]}="{tuple[1]}"', self.props.items()))
    
    def __repr__(self):
        return self.to_html()