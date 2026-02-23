from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        text = strip_block_text(block, block_type)
        if block_type == BlockType.CODE:
            block_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, text)])])
        elif block_type == BlockType.ULIST or block_type == BlockType.OLIST:
            block_node = ParentNode(block_type_to_tag(block_type, block), list_to_list_nodes(text))
        else:
            block_node = ParentNode(block_type_to_tag(block_type, block), text_to_children(text))
        nodes.append(block_node)
    return ParentNode("div", nodes)

def block_type_to_tag(block_type, block):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            heading_num = block.index(" ")
            return f"h{heading_num}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.ULIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
        case _:
            raise Exception("No valid block type found")
        
def strip_block_text(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return block.replace("\n", " ")
        case BlockType.HEADING:
            i = block.find(" ")
            return block[i+1:]
        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.lstrip("> "))
            return " ".join(stripped_lines)
        case BlockType.ULIST:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                i = line.find(" ")
                stripped_lines.append(line[i+1:])
            return stripped_lines
        case BlockType.OLIST:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                i = line.find(" ")
                stripped_lines.append(line[i+1:])
            return stripped_lines
        case BlockType.CODE:
            lines = block.split("\n")
            lines = lines[1:-1]
            return ("\n".join(lines)) + "\n"
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes 

def list_to_list_nodes(lists):
    list_nodes = []
    for line in lists:
        list_nodes.append(ParentNode("li", text_to_children(line)))
    return list_nodes

def extract_title(markdown):
    markdown_split = markdown.split("\n")
    for line in markdown_split:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")

