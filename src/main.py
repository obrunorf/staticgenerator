from generator import prepare_directory, generate_page, generate_pages_recursive
def main():
    prepare_directory()
    from_path = 'content/'
    template_path = 'template.html'
    dest_path = 'public/'
    #generate_page(from_path, template_path, dest_path)
    generate_pages_recursive(from_path, template_path, dest_path)
    

main()