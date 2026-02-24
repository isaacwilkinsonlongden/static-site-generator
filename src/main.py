import os
import shutil
import sys

from markdown_to_html import markdown_to_html_node, extract_title

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    copy_contents(source, destination)

def copy_contents(source, destination):
    file_List = os.listdir(source)
    for file in file_List:
        source_path = os.path.join(source, file)
        destination_path = os.path.join(destination, file)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path) 
            print(f"copied {source_path} to {destination_path}")
        else:
            os.mkdir(destination_path)
            copy_contents(source_path, destination_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    file_list = os.listdir(dir_path_content)
    for file in file_list:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            if file[-3:] == ".md":
                dest_path = dest_path.replace(".md", ".html")
                generate_page(file_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, basepath)
    

if __name__ == "__main__":
    main()