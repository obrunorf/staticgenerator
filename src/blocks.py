from enum import Enum
from node_funcs import markdown_to_blocks, text_to_textnodes, text_to_html_node
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
        if type != BlockType.CODE:
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
            s = text_to_html_node(block.replace('#'*h,""))
            html_node = ParentNode(tag=f'h{h}',children=s)
        
        if type == BlockType.QUOTE:
            s = text_to_html_node(block)
            html_node = ParentNode(tag='blockquote',children=s)
            
        if type == BlockType.ORDRED_LIST:
            html_node = ParentNode('ol',text_to_children(block,2))
        
        if type == BlockType.UNORDERED_LIST:
            html_node = ParentNode('ul',text_to_children(block,1))
        
        if type == BlockType.CODE:
            s = block[3:-3].lstrip('\n')
            subnode = LeafNode(tag='code',value = s)
            html_node = ParentNode('pre', [subnode])
        childs.append(html_node)
    root_node = ParentNode(tag='div', children=childs)
    
    return root_node
            
def text_to_children(text,skip):
    res= []
    for line in text.splitlines():
        s = text_to_html_node(line[skip:])
        res.append(LeafNode('li',s))
    return res