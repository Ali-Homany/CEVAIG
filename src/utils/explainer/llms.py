import re
import json
from typing import Any
from google import genai


"""
This module is responsible for providing LLM to explain code
"""


class Gemini:
    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    def generate(self, prompt: str) -> Any | str:
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-thinking-exp',
            contents=prompt
        )
        json_match = re.search(r'(?s)```json\n(.*?)```', response.text)
        if json_match:
            json_str = json_match.group(1)
            return json.loads(json_str)
        return response.text
