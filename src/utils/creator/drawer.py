import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


"""
This module is responsible for drawing images using pillow.
"""


def load_font(font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
    base_url = 'https://github.com/google/fonts/raw/refs/heads/main/ofl'
    folder_name = font_name.lower().replace(' ', '')
    file_name = font_name.replace(' ', '') + '-Regular.ttf'
    font_url = f'{base_url}/{folder_name}/{file_name}'
    response = requests.get(font_url)
    
    if response.status_code != 200:
        # try another file name
        file_name = font_name.replace(' ', '') + '[wght].ttf'
        font_url = f'{base_url}/{folder_name}/{file_name}'
        response = requests.get(font_url)
    if response.status_code == 200:
        return ImageFont.truetype(BytesIO(response.content), font_size)
    else:
        raise ValueError(f"Could not load font: {font_name}")


def draw_project_cover(
    project_title: str,
    project_subtitle: str,
    width: int=3524,
    height: int=2068,
    font_size: int=300
) -> Image.Image:
    TITLE_MAX_CHARACTERS = 16
    TITLE_SUBTITLE_RATIO = 2.5
    project_title = project_title[:TITLE_MAX_CHARACTERS]
    project_subtitle = project_subtitle[:int(TITLE_MAX_CHARACTERS * TITLE_SUBTITLE_RATIO)]
    # Generate random gradient colors
    start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (width, height), color=start_color)
    draw = ImageDraw.Draw(image)
    # generate gradient
    for x in range(width):
        r = start_color[0] + (end_color[0] - start_color[0]) * x // width
        g = start_color[1] + (end_color[1] - start_color[1]) * x // width
        b = start_color[2] + (end_color[2] - start_color[2]) * x // width
        draw.line((x, 0, x, height), fill=(r, g, b))
    # load font
    font = load_font('Solway', font_size)
    # get text size to center it
    title_width, title_height = draw.textbbox((0, 0), project_title, font=font)[2:4]
    position = ((width - title_width) // 2, (height - title_height) // 2)
    # write text
    draw.text(position, project_title, font=font, fill="black")
    # write subtitle
    font = load_font('Fira Code', font_size // TITLE_SUBTITLE_RATIO)
    text_width, text_height = draw.textbbox((0, 0), project_subtitle, font=font)[2:4]
    position = ((width - text_width) // 2, (height - text_height) // 2 + 100 + title_height)
    draw.text(position, project_subtitle, font=font, fill="rgb(20, 20, 20)")
    return image


def draw_project_tree(
    project_title: str,
    project_tree: str,
    width: int=3524,
    height: int=2068,
) -> Image.Image:
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    # replace directory with project title
    text = '\n'.join([project_title] + project_tree.split('\n')[1:])
    font_size = 1700 // text.count('\n') # magic ratio to make it look good
    font = load_font('Fira Code', font_size)
    # center text
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, font=font, fill="white")
    return image
