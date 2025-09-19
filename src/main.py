from generator import prepare_directory, generate_pages_recursive
import sys

def main():
    basepath =  sys.argv[1] if len(sys.argv) > 1 else '/'
        
    
    from_path = 'content/'
    template_path = 'template.html'
    dest_path = 'docs/'
    #generate_page(from_path, template_path, dest_path)
    prepare_directory('static', dest_path)
    generate_pages_recursive(from_path, template_path, dest_path, basepath)
    

main()