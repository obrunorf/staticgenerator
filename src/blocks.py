from enum import Enum
from node_funcs import markdown_to_blocks, text_to_textnodes, text_to_html_node, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDRED_LIST = 'ordered_list'

def block_to_blocktype(mkdown_block) -> BlockType:
    import re
    if re.match(r'\#+ ', mkdown_block):
        return BlockType.HEADING
    if mkdown_block.startswith('```') and mkdown_block.endswith('```'):
        return BlockType.CODE
    if re.search(r'>.*', mkdown_block) is not None and mkdown_block.count('\n')+1 == len(re.findall(r'>.*', mkdown_block)):
        return BlockType.QUOTE
    
    if re.search(r'- .*', mkdown_block) is not None and mkdown_block.count('\n')+1 == len(re.findall(r'- .*', mkdown_block)):
        return BlockType.UNORDERED_LIST
    
    lines = mkdown_block.splitlines()
    count = 1
    ordered = True
    for line in lines:
        if not line.strip().startswith(f'{count}. '):
            ordered = False
        count += 1
    if ordered:
        return BlockType.ORDRED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    childs = []
    for block in blocks:
        type = block_to_blocktype(block)
        if type != BlockType.CODE and type != BlockType.ORDRED_LIST and type != BlockType.UNORDERED_LIST:
            block = block.replace('\n',' ')
        if type == BlockType.PARAGRAPH:
            s = text_to_html_node(block)
            html_node = ParentNode(tag='p', children=s)
        
        if type == BlockType.HEADING:
            h = 0
            for char in block:
                if char =="#":
                    h+=1
                else:
                    break
            s = text_to_children(block[h+1:])
            html_node = ParentNode(tag=f'h{h}',children=s)
        
        if type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
            
        if type == BlockType.ORDRED_LIST:
            html_node = olist_to_html_node(block)
        
        if type == BlockType.UNORDERED_LIST:
            html_node = ulist_to_html_node(block)
        
        if type == BlockType.CODE:
            s = block[3:-3].lstrip('\n')
            subnode = LeafNode(tag='code',value = s)
            html_node = ParentNode('pre', [subnode])
        childs.append(html_node)
    root_node = ParentNode(tag='div', children=childs)
    
    return root_node
            
def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children