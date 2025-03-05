import os


"""
This module is responsible for wrapping up the codebase for a model
"""


def read_code_file(file_path: str, add_line_numbers: bool=False) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    if add_line_numbers:
        code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(code.split('\n'))])
    return code


def get_codebase(dir_path: str, show_line_numbers: bool=False, allowed_files: list=('py', 'html', 'css', 'md')) -> str:
    codebase = ''
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension in allowed_files:
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, dir_path)
                codebase += f'\n\n{relative_file_path}:\n```\n{read_code_file(file_path, add_line_numbers=show_line_numbers)}\n```\n'
    return codebase


if __name__ == '__main__':
    print(get_codebase('./testing/sample_code/', show_line_numbers=True))
