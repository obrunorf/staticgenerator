from node_funcs import add_tag

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        #if tag:
        self.tag = tag
        #else:
        #   self.tag = None
        if value:
            self.value = value
        if children:
            self.children = children
        if props:
            self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        res = ''
        for attr in self.props:
            res += f' {attr}="{self.props[attr]}"'
        return res
    
    def __repr__(self) -> str:
        res =''
        if hasattr(self,'tag') and self.tag is not None:
            res += f" tag={self.tag} "
        if hasattr(self,'value'):
            res+= f" value ={self.value} "
        if hasattr(self,'children'):
            res += f" children={self.children} "
        if hasattr(self,'props'):
            res += " props=" +self.props_to_html()
        if len(res) ==0:
            res = "err: empty node"
        return res
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        else:
            res = add_tag(self.tag, self.value)
            return res
        
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
    