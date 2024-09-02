import FileFactories
import os
import sys

current_dir_path = '.'
vica_path = os.__file__

def get_arg_value(args, name):
    for i in range(len(args)):
        arg: str = args[i]
        
        if arg == name and i < len(args) -1:
            return args[i+1]
    
    return None

def create_project(proj_name = 'Vica'):
    cmake: str = FileFactories.create_cmake_lists(project=proj_name)
    
    os.mkdir('src')
    os.mkdir('include')
    os.mkdir('deps')
    
    with open('./CMakeLists.txt', 'w') as cmake_file:
        cmake_file.write(cmake)
        
    with open('./src/main.cpp', 'w') as main_file:
        main_file.write(FileFactories.create_main())

def create_header(name: str, namespace: str):
    header = FileFactories.create_header(name, namespace)
    
    with open(f'./include/{name}.h', 'w') as file:
        file.write(header)

def create_definition(name: str, namespace: str):
    definition = FileFactories.create_definitions(name, namespace)
    
    with open(f'./src/{name}.cpp', 'w') as file:
        file.write(definition)
        
def update_cmake(classname: str):
    content: str = None
    with open('./CMakeLists.txt', 'r') as infile:
        content = infile.read(-1)
    
    content = content.replace(
        '#ADD_CPP - DO NOT MODIFY THIS LINE',
        f'${{SRC}}/{classname}.cpp\n' +
        '    #ADD_CPP - DO NOT MODIFY THIS LINE')
    
    with open("./CMakeLists.txt", 'w') as outfile:
        outfile.write(content)
        
def create_class(name: str, namespace: str):
    
    create_header(name, namespace)
    create_definition(name, namespace)
    update_cmake(name)

def main():
    parent_dir_name: str = os.path.basename(os.getcwd())
    if (len(sys.argv) < 2) or (sys.argv[1] == 'create'):
        
        if (len(os.listdir(current_dir_path)) > 0):
            print('Directory is not empty. Quitting.')
            return
        else:
            current_dir: str = parent_dir_name
            create_project(current_dir)
    
    elif sys.argv[1] == 'class':
    
        name: str = get_arg_value(sys.argv, '-name')
        if name is None:
            print('Class name not provided. Please provide a name with \'-name name\'')
            return
        
        namespace: str = get_arg_value(sys.argv, '-namespace')
        if namespace is None:
            namespace = parent_dir_name
        
        create_class(name, namespace)

if __name__ == '__main__':
    main()