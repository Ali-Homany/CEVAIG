import os
from dotenv import load_dotenv
from pydantic import BaseModel
from utils.explainer.codebase_parser import get_codebase
from utils.explainer.llms import Gemini


"""
This package is responsible for explaining a code file into json format
"""


load_dotenv()
curr_dir = os.path.dirname(os.path.abspath(__file__))


class Explanation(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    explanatory_text: str


def explain_codebase(dir_path: str) -> list[dict]:
    codebase_str = get_codebase(dir_path)
    llm = Gemini(os.getenv('GENAI_API_KEY'))
    with open(f'{curr_dir}/prompt_explain.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(codebase=codebase_str)
    explanations = llm.generate(prompt)
    # explanations = [explanation.dict() for explanation in explanations]
    return explanations


def add_highlighting(dir_path: str, explanations: list[dict], max_highlight: int=30) -> list[dict]:
    codebase_str = get_codebase(dir_path, show_line_numbers=True)
    llm = Gemini(os.getenv('GENAI_API_KEY'))
    with open(f'{curr_dir}/prompt_highlight.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(codebase=codebase_str, explanations=explanations, max_highlight=max_highlight)
    updated_explanations = llm.generate(prompt)
    return updated_explanations
