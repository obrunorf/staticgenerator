from enum import Enum

class TextType(Enum):
    PLAIN = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC ="_Italic text_"
    CODE = '`Code text`'
    LINK = "Links, in this format: [anchor text](url)"
    IMAGE= "Images, in this format: ![alt text](url)"

    
class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, __value) -> bool:
        try:
            if self.text == __value.text and self.text_type == __value.text_type and self.url == __value.url:
                return True
            return False
        except:
            return False
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'