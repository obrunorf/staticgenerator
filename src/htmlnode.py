from node_funcs import add_tag

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ''
        res = ''
        for attr in self.props:
            res += f' {attr}="{self.props[attr]}"'
        return res
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
       if self.value is None:
           raise ValueError
       if self.tag is None:
           return self.value
       return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("children-less")
        
        res = ''
        for c in self.children:
            res+= c.to_html()
        return add_tag(self.tag, res)
    