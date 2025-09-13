#helper constant dicts
textype_to_html_tag ={
    'PLAIN'  : "",
    'BOLD'   : "b",
    'ITALIC' : "i",
    'CODE'   : 'code',
    'LINK'   : "a",
    'IMAGE'  : "img"
}

textype_to_delimiter ={ #this might be unecessary, maybe delete?
    'BOLD'   : "**",
    'ITALIC' : "_",
    'CODE'   : '`'
}

def add_tag(tag, text):
    return f"<{tag}>{text}</{tag}>"

def text_node_to_html_node(text_node):
        from htmlnode import LeafNode
        from textnode import TextType
        if text_node.text_type.value not in TextType._value2member_map_:
            raise ValueError
        
        if text_node.text_type == TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        tag = textype_to_html_tag[text_node.text_type.name]
        
        if tag == 'a':
            return LeafNode(tag=tag, value=text_node.text, props={'href':text_node.url})
        if tag == 'img':
            return LeafNode(tag=tag, value='', props={'src': text_node.url,
                    'alt': text_node.text})
        return LeafNode(tag=tag, value=text_node.text)
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextType, TextNode
    processed_nodes = []
    step = len(delimiter)
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            processed_nodes.append(node)
        else:
            ocurrences = [i for i in range(len(node.text)) if node.text.startswith(delimiter, i)]
            if len(ocurrences) % 2 != 0:
                raise Exception(f'Invalid markdown input {node.text}')
            mkdowns = []
            #print(ocurrences)
            for x in range(0,len(ocurrences),2):
                mkdowns.append(node.text[ocurrences[x]+step:ocurrences[x+1]])
                #print('appending')
                #print(node.text[ocurrences[x]+step:ocurrences[x+1]])
                
            #print(mkdowns)
            for part in node.text.split(delimiter):
                if len(part) == 0:
                    continue
                if part in mkdowns:
                    processed_nodes.append(TextNode(part, text_type))
                else:
                    processed_nodes.append(TextNode(part, TextType.TEXT))
    return processed_nodes

def extract_markdown_images(text):
    import re
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    from textnode import TextNode, TextType
    processed_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            processed_nodes.append(node)
            continue
        s = node.text
        for m in matches:
            image_alt, image_link = m
            sections = s.split(f"![{image_alt}]({image_link})",1)
            if len(sections[0]) >0:
                processed_nodes.append(TextNode(sections[0],TextType.TEXT)) #this is the text pre link
            processed_nodes.append(TextNode(image_alt,TextType.IMAGE,image_link))
            if len(sections) > 1:
                s = sections[1]#the rest
            else:
                s = ''
        if s != '':
            processed_nodes.append(TextNode(s,TextType.TEXT))
            
    return processed_nodes

def split_nodes_link(old_nodes):
    from textnode import TextNode, TextType
    processed_nodes =[]
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            processed_nodes.append(node)
            continue
        s = node.text
        for m in matches:
            anchor, link = m
            sections = s.split(f"[{anchor}]({link})",1)
            if len(sections[0]) >0:
                processed_nodes.append(TextNode(sections[0],TextType.TEXT)) #this is the text pre link
            processed_nodes.append(TextNode(anchor,TextType.LINK,link))
            if len(sections) > 1:
                s = sections[1]#the rest
            else:
                s = ''
        if s != '':
            processed_nodes.append(TextNode(s,TextType.TEXT))
    return processed_nodes

def text_to_textnodes(text):
    from textnode import TextNode, TextType
    #split along lines for readability
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    processed_blocks =[]
    for block in blocks:
        #s = block.replace('\n',' ')
        s = block.strip()
        if len(s) > 0 :
            processed_blocks.append(s)
    return processed_blocks

def text_to_html_node(text):
    nodes =  text_to_textnodes(text)
    htmls = []
    for node in nodes:
        htmls.append(text_node_to_html_node(node))
    return htmls