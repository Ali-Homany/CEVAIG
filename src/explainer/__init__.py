import os
from dotenv import load_dotenv
from pydantic import BaseModel
from explainer.codebase_parser import get_codebase
from explainer.llms import Gemini


"""
This package is responsible for explaining a code file into json format
"""


load_dotenv()


class Explanation(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    explanatory_text: str


def explain_codebase(dir_path: str) -> str:
    codebase_str = get_codebase(dir_path)
    llm = Gemini(os.getenv('GENAI_API_KEY'))
    with open('./src/explainer/prompt_explain.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(codebase=codebase_str)
    explanations = llm.generate(prompt, response_schema=list[Explanation])
    # explanations = [explanation.dict() for explanation in explanations]
    return explanations


def add_highlighting(dir_path: str, explanations: list[dict], max_highlight: int=30) -> list[dict]:
    codebase_str = get_codebase(dir_path, show_line_numbers=True)
    llm = Gemini(os.getenv('GENAI_API_KEY'))
    with open('./src/explainer/prompt_highlight.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(codebase=codebase_str, explanations=explanations, max_highlight=max_highlight)
    updated_explanations = llm.generate(prompt, response_schema=list[Explanation])
    return updated_explanations


if __name__ == '__main__':
    import json
    explanations = explain_codebase(
        './testing/sample_code/'
    )
    with open('./temp/explanations.json', 'w') as f:
        json.dump(explanations, f, indent=4)
    explanations = add_highlighting(
        './testing/sample_code/',
        explanations
    )
    with open('./temp/explanations_2.json', 'w') as f:
        json.dump(explanations, f, indent=4)
