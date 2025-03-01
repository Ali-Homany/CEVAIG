import os
import json
import tempfile
import subprocess
from PIL import Image

"""
This package is responsible for taking a screenshot of a code file.
"""


TEMP_DIR = './temp/'
# path to preset
CARBON_PRESET_PATH = os.path.join(os.path.expanduser('~'), '.carbon-now.json')
SCRIPT_TEMPLATE = """
@echo off
REM Run carbon-now non-interactively with preset options on a file
carbon-now {file_path}"
pause
"""


def get_carbon_script(
        code: str,
        file_path: str,
        highlight_start: int=None,
        highlight_num_lines: int=None,
        font_name: str='Space Mono',
        style_name: str='dracula',
        starting_line: int=1,
    ) -> str:
    num_lines = len(code.split('\n'))
    with open(CARBON_PRESET_PATH, 'r') as f:
        preset = json.load(f)
    preset['latest-preset']['fontFamily'] = font_name
    preset['latest-preset']['theme'] = style_name
    if highlight_start:
        preset['latest-preset']['selectedLines'] = ','.join(
            map(str, list(range(highlight_start, min(highlight_start + highlight_num_lines, num_lines))))
        )
    else:
        preset['latest-preset']['selectedLines'] = '*'
    preset['latest-preset']['lineNumbers'] = "true"
    preset['latest-preset']['firstLineNumber'] = starting_line
    with open(CARBON_PRESET_PATH, 'w') as f:
        json.dump(preset, f, indent=4)
    return SCRIPT_TEMPLATE.format(file_path=file_path)


def create_temp_file(content, suffix: str) -> str:
    content = content.strip()
    with tempfile.NamedTemporaryFile('w', delete=False, suffix=suffix) as file:
        file.write(content)
        file.flush()
        file_path = file.name
    return file_path


def get_image_from_path(image_path: str) -> Image.Image:
    img = Image.open(image_path)
    img.load()
    img_output = img.copy()
    img.close()
    return img_output


def create_screenshot(
        code: str,
        file_rel_path: str=None,
        highlight_start: int=None,
        highlight_num_lines: int=1,
        font_name: str='Space Mono',
        style_name: str='dracula',
        max_lines: int=40
    ) -> Image.Image:
    num_lines = len(code.split('\n'))
    if num_lines > max_lines:
        if not highlight_start:
            code = '\n'.join(code.split('\n')[:max_lines])
            starting_line = 1
        else:
            num_lines_around = (max_lines - highlight_num_lines) // 2
            starting_line = max(highlight_start - num_lines_around, 1)
            ending_line = min(highlight_start + highlight_num_lines + 1 + num_lines_around, num_lines)
            code = '\n'.join(code.split('\n')[starting_line:ending_line])
            highlight_start -= starting_line
            highlight_num_lines = min(highlight_num_lines, ending_line - highlight_start)
    # save code to temporary file
    file_path = f'{TEMP_DIR}/{file_rel_path}' if file_rel_path else f'{TEMP_DIR}/code'
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(code)
        f.flush()
    # pass parameters to script
    script = get_carbon_script(
        code, file_path,
        highlight_start, highlight_num_lines,
        font_name, style_name, starting_line
    )
    # save script to batch temp file
    script_path = create_temp_file(script, suffix='.bat')
    # run script
    subprocess.run(script_path, check=True)
    # get screenshot path
    screenshot_path = max([f for f in os.listdir('./') if f.endswith('.png')], key=os.path.getmtime)
    # load screenshot
    image_output = get_image_from_path(screenshot_path)
    # cleanup, remove temp files
    os.remove(file_path)
    os.remove(script_path)
    os.remove(screenshot_path)
    return image_output


if __name__ == '__main__':
    file_path = './testing/sample_code/nb_generator.py'
    with open(file_path, 'r') as f:
        code = f.read()
    img = create_screenshot(
        code=code,
        highlight_start=10,
        highlight_num_lines=3,
        file_rel_path=file_path.split('/')[-1],
        font_name='Space Mono',
        style_name='dracula'
    )
    img.show()
