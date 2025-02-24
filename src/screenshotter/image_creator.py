import io
from PIL import Image
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name


def create_screenshot(
    code: str,
    highlight_start: int=None,
    highlight_num_lines: int=1,
    font_name: str='Space Mono',
    style_name: str='dracula',
    ) -> Image.Image:
    style = get_style_by_name(style_name)
    formatter = ImageFormatter(
        font_name=font_name,
        style=style,
        line_numbers=True,
        hl_lines=list(range(highlight_start, highlight_start + highlight_num_lines)),
        line_number_bg='#2e2e2e',
        line_number_fg='#f8f8f2',
        background='#272822',
        padding=10,
        image_dpi=300,  # Higher DPI for better quality
        font_size=18  # Larger font for readability
    )
    img_data = highlight(code, PythonLexer(), formatter)
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)  # Scale up smoothly
    return img


def crop_code_image(img, highlight_start, total_lines, max_lines_around=25):
    line_height = img.height // total_lines
    img = img.crop((
        0,
        max((highlight_start - max_lines_around) * line_height, 0),
        img.width,
        min((highlight_start + max_lines_around) * line_height, img.height)
    ))
    return img


if __name__ == '__main__':
    with open('./src/screenshotter/image_creator.py', 'r') as f:
        code = f.read()
    img = create_screenshot(
        code=code,
        highlight_start=10,
        highlight_num_lines=3
    )
    img.show()
