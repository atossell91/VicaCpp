from VicaFile import VicaFile
from VicaFile import parse_file
from VicaFile import build_file_text

import os

vica_path = os.path.dirname(__file__)

cmake_lists_file_path = f'{vica_path}/CMakeLists.txt.vica'
main_file_path = f'{vica_path}/main.cpp.vica'
header_file_path = f'{vica_path}/header.h.vica'
interface_file_path = f'{vica_path}/interface.h.vica'
namespace_file_path = f'{vica_path}/namespace.h.vica'
definition_file_path = f'{vica_path}/definition.cpp.vica'

def load_file_text(filepath: str) -> str:
    content: str = None
    with open(filepath, 'r') as file:
        content = file.read(-1)
    return content
    

def create_cmake_lists(project:str = "Vica", version: str = '3.11.2') -> str:
    content: str = load_file_text(cmake_lists_file_path)
    vf = parse_file(content)
    
    vf.variables['project'] = project
    vf.variables['version'] = version
    
    return build_file_text(vf)


def create_main() -> str:
    content: str = load_file_text(main_file_path)
    vf = parse_file(content)
    
    # Set variables here
    
    return build_file_text(vf)


def create_namespace(name: str) -> str:
    content: str = load_file_text(namespace_file_path)
    vf = parse_file(content)
    
    # Set variables here
    vf.variables['namespace'] = name
    
    return build_file_text(vf)


## Lots of duplicated code! (header, interface and definitions below)
def create_header(name: str, namespace: str) -> str:
    content: str = load_file_text(header_file_path)
    vf = parse_file(content)
    
    # Set variables here
    vf.variables['classname'] = name
    vf.variables['namespace'] = namespace
    
    return build_file_text(vf)


def create_interface(name: str, namespace: str) -> str:
    content: str = load_file_text(interface_file_path)
    vf = parse_file(content)
    
    # Set variables here
    vf.variables['classname'] = name
    vf.variables['namespace'] = namespace
    
    return build_file_text(vf)


def create_definitions(name: str, namespace: str, folder: str = None) -> str:
    content: str = load_file_text(definition_file_path)
    vf = parse_file(content)
    
    # Set variables here
    vf.variables['classname'] = name
    vf.variables['namespace'] = namespace
    
    if not folder is None:
        vf.variables['folder'] = f'{folder}/'
    else:
        vf.variables['folder'] = ''
    
    return build_file_text(vf)
