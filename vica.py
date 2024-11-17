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

def create_folder_str(folder: str):
    if folder is None:
        return ''
    else:
        return f'{folder}/'

def create_project(proj_name = 'Vica'):
    cmake: str = FileFactories.create_cmake_lists(project=proj_name)
    
    os.mkdir('src')
    os.mkdir('include')
    os.mkdir('deps')
    
    with open('./CMakeLists.txt', 'w') as cmake_file:
        cmake_file.write(cmake)
        
    with open('./src/main.cpp', 'w') as main_file:
        main_file.write(FileFactories.create_main())

def create_header(name: str, namespace: str, folder: str = None):
    header = FileFactories.create_header(name, namespace)
        
    folderStr: str = create_folder_str(folder)
    
    with open(f'./include/{folderStr}{name}.h', 'w') as file:
        file.write(header)

def create_interface(name: str, namespace: str, folder: str = None):
    interface = FileFactories.create_interface(name, namespace)
        
    folderStr: str = create_folder_str(folder)
    
    with open(f'./include/{folderStr}{name}.h', 'w') as file:
        file.write(interface)

def create_namespace(name: str, folder: str = None):
    namespace = FileFactories.create_namespace(name)
        
    folderStr: str = create_folder_str(folder)
    
    with open(f'./include/{folderStr}{name}.h', 'w') as file:
        file.write(namespace)

def create_definition(name: str, namespace: str, folder: str = None):
    definition = FileFactories.create_definitions(name, namespace, folder)
        
    folderStr: str = create_folder_str(folder)
    
    with open(f'./src/{folderStr}{name}.cpp', 'w') as file:
        file.write(definition)
        
def update_cmake(classname: str, folder: str = None):
    content: str = None
        
    folderStr: str = create_folder_str(folder)
        
    with open('./CMakeLists.txt', 'r') as infile:
        content = infile.read(-1)
    
    content = content.replace(
        '#ADD_CPP - DO NOT MODIFY THIS LINE',
        f'${{SRC}}/{folderStr}{classname}.cpp\n' +
        '    #ADD_CPP - DO NOT MODIFY THIS LINE')
    
    with open("./CMakeLists.txt", 'w') as outfile:
        outfile.write(content)
        
def create_class(name: str, namespace: str, folder: str):
    
    create_header(name, namespace, folder)
    create_definition(name, namespace, folder)
    update_cmake(name, folder)

def get_name():
    return get_arg_value(sys.argv, '-name')

def get_dest_folder():
    return get_arg_value(sys.argv, '-folder')

def get_namespace():
    return get_arg_value(sys.argv, '-namespace')

def main():
    parent_dir_name: str = os.path.basename(os.getcwd())
    if (len(sys.argv) < 2) or (sys.argv[1] == 'create'):
        
        if (len(os.listdir(current_dir_path)) > 0):
            choice: str = input('Directory is not empty. Enter \'ok\' to continue: ')
            if (choice.lower() != 'ok'):
                print ('Stopping')
                return
            
        current_dir: str = parent_dir_name
        create_project(current_dir)
    
    elif sys.argv[1] == 'subdir':
        name: str = get_name()
        
        if name is None:
            print('Folder name not provided. Please provide a name.')
            return
        
        folder: str = get_dest_folder()
        folderStr: str = create_folder_str(folder)
        
        suffix: str = f'/{folderStr}{name}'
        
        os.mkdir(f'src/{suffix}')
        os.mkdir(f'include/{suffix}')
            
    elif sys.argv[1] == 'namespace':
        name: str = get_name()
        folder: str = get_dest_folder()
        if name is None:
            print('Interface name not provided. Please provide a name with \'-name name\'')
            return
        
        create_namespace(name, folder)
            
    ## Duplicated code (see 'class' below)!
    elif sys.argv[1] == 'header':
        name: str = get_name()
        folder: str = get_dest_folder()
        if name is None:
            print('Class name not provided. Please provide a name with \'-name name\'')
            return
        
        namespace: str = get_namespace()
        folder: str = get_dest_folder()
        if namespace is None:
            namespace = parent_dir_name
        
        create_header(name, namespace, folder)
            
    elif sys.argv[1] == 'interface':
        name: str = get_name()
        if name is None:
            print('Interface name not provided. Please provide a name with \'-name name\'')
            return
        
        folder: str = get_dest_folder()
        namespace: str = get_namespace()
        if namespace is None:
            namespace = parent_dir_name
        
        create_interface(name, namespace, folder)
    
    elif sys.argv[1] == 'class':
    
        name: str = get_name()
        if name is None:
            print('Class name not provided. Please provide a name with \'-name name\'')
            return
        
        folder: str = get_dest_folder()
        namespace: str = get_namespace()
        if namespace is None:
            namespace = parent_dir_name
        
        create_class(name, namespace, folder)

if __name__ == '__main__':
    main()