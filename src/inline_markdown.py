import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("No closing delimiter found")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_images = extract_markdown_images(node.text)
            if len(extracted_images) == 0:
                new_nodes.append(node)
                continue
            text = node.text
            for i in range(len(extracted_images)):
                sections = text.split(f"![{extracted_images[i][0]}]({extracted_images[i][1]})", 1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown image syntax")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(extracted_images[i][0], TextType.IMAGE, extracted_images[i][1]))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_links(node.text)
            if len(extracted_links) == 0:
                new_nodes.append(node)
                continue
            text = node.text
            for i in range(len(extracted_links)):
                sections = text.split(f"[{extracted_links[i][0]}]({extracted_links[i][1]})", 1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown link syntax")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes



