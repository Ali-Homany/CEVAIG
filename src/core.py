import os
import json
import random
import asyncio
import numpy as np
from PIL import Image
from utils.video_utils import merge_all
from utils.tts import SpeechTextConverter, preprocess_text, save_audio_to_file
from utils.creator.screenshotter import create_screenshot
from utils.explainer import explain_codebase, add_highlighting
from utils.explainer.codebase_parser import generate_codebase_tree
from utils.creator.drawer import draw_project_cover, draw_project_tree


# DEFINE DIRS
curr_dir = os.path.abspath(os.path.dirname(__file__))
# where the project we wanna explain is
PROJECT_DIR = 'project'
os.path.exists(PROJECT_DIR) or os.makedirs(PROJECT_DIR)
# where we store static files like images
STATIC_DIR = f'{curr_dir}/static'
os.path.exists(STATIC_DIR) or os.makedirs(STATIC_DIR)
# temp dir for caching explanations & screenshots
CACHE_DIR = f'{curr_dir}/temp/test_{random.randint(0, 10000)}/'
os.path.exists(CACHE_DIR) or os.makedirs(CACHE_DIR)


def get_explanations(
    num: int=20,
    ignored_files: list[str]=None,
    user_instructions: str='',
    use_cache: bool=True,
) -> list[dict]:
    # generate explanations (or read cache)
    if use_cache and os.path.exists(f'{CACHE_DIR}../explanations.json'):
        with open(f'{CACHE_DIR}../explanations.json', 'r') as file:
            explanations = json.load(file)
    else:
        explanations = explain_codebase(PROJECT_DIR, ignored_files, num, user_instructions)
        explanations = add_highlighting(PROJECT_DIR, ignored_files=ignored_files, explanations=explanations)
        with open(f'{CACHE_DIR}explanations.json', 'w') as file:
            json.dump(explanations, file, indent=4)
    return explanations


async def _generate_images(
    explanations: list[dict],
    title: str,
    subtitle: str,
    project_dir: str
) -> list[np.ndarray]:
    images = []
    cover_image, dir_image = None, None
    for i, item in enumerate(explanations):
        if item['file_path'] == '' or item['file_path'] == '.' or item['file_path'] is None or item['file_path'] == '0':
            img = await asyncio.to_thread(
                draw_project_cover,
                project_title=title, project_subtitle=subtitle
            ) if not cover_image else cover_image
        # if directory
        elif item['file_path'] == './' or os.path.isdir(os.path.normpath(item['file_path'])):
            img = await asyncio.to_thread(
                draw_project_tree,
                title, generate_codebase_tree(project_dir)
            ) if not dir_image else dir_image
        # if file
        else:
            item['file_path'] = os.path.join(PROJECT_DIR, item['file_path'])
            item['code'] = open(item['file_path'], 'r').read()
            if not item['start_line'] or item['start_line'] < 2:
                item['start_line'] = None
            try:
                img = await asyncio.to_thread(
                    create_screenshot,
                    code=item['code'],
                    cache_dir=CACHE_DIR,
                    file_rel_path=os.path.relpath(item['file_path'], PROJECT_DIR),
                    highlight_start=item['start_line'],
                    highlight_num_lines=(item['end_line'] - item['start_line'] + 1) if item['start_line'] else None
                )
            except Exception as e:
                print(f'file {item["file_path"]} failed to generate screenshot: {e}')
                img = Image.new('RGB', (3524, 2068), color=(0, 0, 0))
        images.append(np.array(img))
        img.save(f'{CACHE_DIR}{i}.png')
        print(f'Created screenshot for {i}.png')
    return images


async def _generate_audios(
    tts: SpeechTextConverter,
    explanations: list[dict]
) -> tuple:
    audios = []
    for i, item in enumerate(explanations):
        # create audio
        sr, audio_np = await asyncio.to_thread(
            tts.str_to_audio,
            preprocess_text(item['explanatory_text'])
        )
        audios.append(audio_np)
        save_audio_to_file(audio_np, sr, f'{CACHE_DIR}{i}.mp3')
        print(f'Created audio for {i}.mp3')
    return audios, sr


def generate_video(
    tts: SpeechTextConverter,
    explanations: list[dict],
    title: str,
    subtitle: str
):
    """Generate video from explanations using the video pipeline"""
    async def generate():
        images, (audios, sr) = await asyncio.gather(
            _generate_images(explanations, title, subtitle, PROJECT_DIR),
            _generate_audios(tts, explanations),
        )
        return merge_all(audios, images, sr)
    return asyncio.run(generate())
