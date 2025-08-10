import os
import re
import shutil
import base64
import requests
from git import Repo
from core import (
    PROJECT_DIR,
    STATIC_DIR
)


def copy_local_folder(folder_dir):
    """Copy a local project folder into the project directory"""
    try:
        shutil.copytree(folder_dir, PROJECT_DIR, dirs_exist_ok=True)
    except Exception as e:
        print(f"Error copying folder {folder_dir} into project directory: {e}")


def is_valid_github_repo_url(url):
    """Returns whether a given url is a valid github repo url"""
    # check url format
    pattern = r'^https://github\.com/[^/]+/[^/]+/?$'
    if not re.match(pattern, url):
        return False
    # check if repo exists, try access it
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error accessing repo {url}: {e}")
        return False


def clone_github_repo(repo_url):
    """Clone a github repo into the project directory"""
    try:
        if os.path.exists(PROJECT_DIR):
            # raise Exception(f"The destination path '{PROJECT_DIR}' already exists.")
            shutil.rmtree(PROJECT_DIR)
            print(f"Deleted existing project directory: {PROJECT_DIR}")
        Repo.clone_from(repo_url, PROJECT_DIR, allow_unsafe_options=True, allow_unsafe_protocols=True)
        return PROJECT_DIR
    except Exception as e:
        raise Exception(f"Failed to clone repository: {e}")


def get_app_styling():
    with open(f"{STATIC_DIR}/styling.css", "r") as f:
        styling = f.read()
    return styling


def read_logo_image() -> str:
    """Reads the logo image and returns it as a base64 string"""
    with open(f"{STATIC_DIR}/logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
    return logo_b64


def get_files_types() -> list[str]:
    """Gets unique file types in the given project"""
    folders_to_ignore = [
        'node_modules', '.git',
        'venv', '.venv', '__pycache__',
        '.pytest_cache', '.vscode',
        'build', 'dist', '.mypy_cache',
        '.ipynb_checkpoints',
    ]
    extensions = set()
    for root, folders, files in os.walk(PROJECT_DIR):
        for ignored_folder in folders_to_ignore:
            if ignored_folder in folders:
                folders.remove(ignored_folder)
        for file in files:
            if '.' in file:
                ext = file.split('.')[-1]
                extensions.add(ext)
    return list(extensions)
