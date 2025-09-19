import os
import shutil
from pathlib import Path

def delete_dest(dest):
    #cleans up destination completely, preparing it for the generation
    shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    

def copy_contents_recursively(origin, destination):
    #welp, thats self explanatory no?
    shutil.copytree(origin, destination, dirs_exist_ok=True)
    
def prepare_directory():
    script_path = Path(__file__).resolve()
    parent_directory = script_path.parent.parent
    target = os.path.join(parent_directory,'public')
    origin = os.path.join(parent_directory,'static')
    delete_dest(target)
    copy_contents_recursively(origin,target)
    
def extract_title(markdown):
    import re
    try:
        res =  re.search(r'^\# (.+)', markdown, re.M).group(1)
    except:
        raise Exception("invalid or non present h1 tag")
    return res

def get_content(filepath):
    file = open(filepath, "r")
    content = file.read()
    file.close()
    return content

def generate_page(from_path, template_path, dest_path):
    from blocks import markdown_to_html_node
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    content = get_content(from_path)
    template = get_content(template_path)
    processed_content = markdown_to_html_node(content)
    processed_content = processed_content.to_html()
    title = extract_title(content)
    html_content = template.replace(r'{{ Title }}',title).replace(r'{{ Content }}', processed_content)
    
    from pathlib import Path
    output_file = Path(dest_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, 'w') as file:
        file.write(html_content)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = get_files_recursive(dir_path_content)
    for file in files:
        if file.endswith('.md'):
            gen_path = file.replace(dir_path_content,dest_dir_path).replace('.md','.html')
            print(gen_path)
            generate_page(file,template_path,gen_path)
            

def get_files_recursive(path='content/'):
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            files.extend(get_files_recursive(full_path))
        else:
            files.append(full_path)  
    return files

files = get_files_recursive()
for file in files:
    print(file)