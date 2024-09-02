import re

class VicaFile:
    def __init__(self):
        self.template_text : str = None
        self.variables = {}

def parse_file(text: str) -> VicaFile:
    file = VicaFile()

    file.template_text = text
    
    matches = re.findall('\@([a-zA-Z0-9._-]+)\@', file.template_text)
    for match in matches:
        key: str = match
        file.variables[key] = ''
    
    return file

def build_file_text(file : VicaFile) -> str:
    output = file.template_text
    for key in file.variables:
        output = output.replace(f'@{key}@', file.variables[key])
        
    return output
