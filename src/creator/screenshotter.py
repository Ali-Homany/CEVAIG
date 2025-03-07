import os
import json
import tempfile
import subprocess
from PIL import Image


"""
This module is responsible for taking a screenshot of a code file.
"""


TEMP_DIR = os.path.abspath('./temp/')
# path to preset
CARBON_PRESET_PATH = os.path.join(os.path.expanduser('~'), '.carbon-now.json')
SCRIPT_TEMPLATE = """
@echo off
REM Run carbon-now non-interactively with preset options on a file
cd "{dir_path}"
carbon-now "{file_name}"
pause
"""


def get_carbon_script(
    code: str,
    file_path: str,
    highlight_start: int=None,
    highlight_num_lines: int=None,
    font_name: str='Space Mono',
    style_name: str='One Dark',
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
    file_path = os.path.abspath(file_path)
    print(f'Script: {SCRIPT_TEMPLATE.format(dir_path=os.path.dirname(file_path), file_name=os.path.basename(file_path))}')
    return SCRIPT_TEMPLATE.format(
        dir_path=os.path.dirname(file_path),
        file_name=os.path.basename(file_path)
    )


def create_temp_file(content: str, suffix: str) -> str:
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
    img_output = img_output.convert("RGB")
    img.close()
    return img_output


def crop_code_columns(code: str) -> str:
    # this method formats code for screenshots
    # make all lines the same length
    NUM_COLUMNS = 160
    code_lines = code.split('\n')
    num_lines = len(code_lines)
    for i, code_line in enumerate(code_lines):
        # pad with spaces
        if len(code_line) < NUM_COLUMNS:
            code_lines[i] += ' ' * (NUM_COLUMNS - len(code_line))
        # truncate extra long lines
        else:
            code_lines[i] = code_line[:NUM_COLUMNS]
    code = '\n'.join(code_lines)
    return code


def crop_code_lines(
    code: str,
    highlight_start: int,
    highlight_num_lines: int,
    max_lines: int,
) -> tuple:
    """
    This method crops code to a certain number of lines, determined by max_lines and highlights.
    Return modified code, start and highlight_start
    """
    num_lines = len(code.split('\n'))
    start = 0
    end = max_lines
    if num_lines > max_lines and highlight_start:
        num_lines_around = (max_lines - highlight_num_lines) // 2
        if highlight_start <= num_lines_around:
            start = 0
        else:
            start = highlight_start - num_lines_around
        end = start + max_lines
        highlight_start -= start
    # crop to start and end
    if end > num_lines:
        code_lines = code.split('\n')[start:] + [' ' for _ in range(end - num_lines)]
        code = '\n'.join(code_lines)
    else:
        code = '\n'.join(code.split('\n')[start:end])
    return code, start, highlight_start


def create_screenshot(
    code: str,
    file_rel_path: str=None,
    highlight_start: int=None,
    highlight_num_lines: int=1,
    font_name: str='Space Mono',
    style_name: str='One Dark',
    max_lines: int=40
) -> Image.Image:
    code, start, highlight_start = crop_code_lines(code, highlight_start, highlight_num_lines, max_lines)
    code = crop_code_columns(code)
    # save code to temporary file
    file_path = os.path.join(TEMP_DIR, file_rel_path or 'code.py')
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(code)
        f.flush()
    # pass parameters to script & save
    script = get_carbon_script(
        code, file_path,
        highlight_start, highlight_num_lines,
        font_name, style_name, starting_line=start+1
    )
    script_path = create_temp_file(script, suffix='.bat')
    # run script
    subprocess.run(script_path, check=True)
    # load screenshot
    screenshot_path = max(
        [os.path.join(os.path.dirname(file_path), f) for f in os.listdir(os.path.dirname(file_path)) if f.endswith('.png')],
        key=os.path.getmtime
    )
    # screenshot_path = os.path.join(os.path.dirname(file_path), screenshot_path)
    image_output = get_image_from_path(screenshot_path)
    # cleanup, remove temp files
    for file in (screenshot_path, script_path, file_path):
        os.remove(file)
    return image_output


if __name__ == '__main__':
    code = 'print("hello world")\nprint("hello world")\nprint("hello world")'
    img = create_screenshot(
        code,
        file_rel_path='main.py',
    )
    img.show()
