def markdown_to_blocks(markdown):
    blocks_unstripped = markdown.split("\n\n")
    blocks = []
    for block in blocks_unstripped:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks
    
    