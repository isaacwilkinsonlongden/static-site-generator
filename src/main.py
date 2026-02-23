import os
import shutil

from textnode import TextNode, TextType

def main():
    static_to_public("static", "public")

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



if __name__ == "__main__":
    main()