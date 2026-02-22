from enum import Enum

def markdown_to_blocks(markdown):
    blocks_unstripped = markdown.split("\n\n")
    blocks = []
    for block in blocks_unstripped:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(markdown_block):
    if markdown_block.startswith((
        "###### ",
        "##### ",
        "#### ",
        "### ",
        "## ",
        "# "
    )):
        return BlockType.HEADING
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    lines = markdown_block.split("\n")
    ol_num = 1
    if lines[0].startswith(">"):
        current = "quote"
    elif lines[0].startswith("- "):
        current = "ul"
    elif lines[0].startswith(f"{ol_num}. "):
        current = "ol"
        ol_num += 1
    else:
        return BlockType.PARAGRAPH
    if current == "quote":
        for i in range(1, len(lines)):
            if lines[i].startswith(">"):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if current == "ul":
        for i in range(1, len(lines)):
            if lines[i].startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if current == "ol":
        for i in range(1, len(lines)):
            if lines[i].startswith(f"{ol_num}. "):
                ol_num += 1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.OLIST

        


    
    