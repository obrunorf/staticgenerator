class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        if tag:
            self.tag = tag
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
        if hasattr(self,'tag'):
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
        