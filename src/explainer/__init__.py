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
    with open('./src/explainer/prompt.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(codebase=codebase_str)
    explanations = llm.generate(prompt, response_schema=list[Explanation])
    # explanations = [explanation.dict() for explanation in explanations]
    return explanations
