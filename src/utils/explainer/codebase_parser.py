import os
from directory_tree import DisplayTree


"""
This module is responsible for parsing a codebase, mainly to wrap it for a model
"""


def generate_codebase_tree(project_dir: str) -> str:
    return DisplayTree(project_dir, stringRep=True).replace('\n', '\n\n')


def read_code_file(file_path: str, add_line_numbers: bool=False) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    if add_line_numbers:
        code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(code.split('\n'))])
    return code


def get_codebase(
    dir_path: str, show_line_numbers: bool=False,
    ignored_files: list[str]=None
) -> str:
    files_ignored_by_default = [
        'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'bmp',
        'pyc', 'pyo', 'pyd', 'pyclass', 'pyo',
        'mp3', 'wav', 'ogg', 'flac', 'mid', 'midi', 'wma',
        'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'tar.gz', 'tgz',
        'exe', 'msi', 'dll', 'so', 'dylib', 'lib', 'a', 'o', 'log',
        'pdf', 'csv', 'tsv', 'xml', 'json', 'ipynb'
    ]
    folders_to_ignore = [
        'node_modules', '.git',
        'venv', '.venv', '__pycache__',
        '.pytest_cache', '.vscode',
        'build', 'dist', '.mypy_cache',
        '.ipynb_checkpoints',
    ]
    if not ignored_files:
        ignored_files = []
    ignored_files += files_ignored_by_default
    codebase = ''
    for root, folders, files in os.walk(dir_path):
        for ignored_folder in folders_to_ignore:
            if ignored_folder in folders:
                folders.remove(ignored_folder)
        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension not in ignored_files:
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, dir_path)
                codebase += f'\n\n{relative_file_path}:\n'
                codebase += f'```\n{read_code_file(file_path, add_line_numbers=show_line_numbers)}\n```\n'
    return codebase
