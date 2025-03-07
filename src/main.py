import os
import json
import random
import asyncio
import numpy as np
from PIL import Image
from explainer import explain_codebase, add_highlighting
from explainer.codebase_parser import generate_codebase_tree
from creator.screenshotter import create_screenshot
from creator.drawer import draw_project_cover, draw_project_tree
from tts import SpeechTextConverter, preprocess_text, save_audio_to_file
from video_utils import merge_all


temp_dir = f'./temp/test_{random.randint(0, 1000)}/'
os.path.exists(temp_dir) or os.makedirs(temp_dir)
test_dir = './testing/sample_code/'


def get_explanations(use_cache: bool=True) -> list[dict]:
    # generate explanations (or read cache)
    if use_cache and os.path.exists(f'{temp_dir}../explanations.json'):
        with open(f'{temp_dir}../explanations.json', 'r') as file:
            explanations = json.load(file)
    else:
        explanations = explain_codebase(test_dir)
        explanations = add_highlighting(test_dir, explanations)
        with open(f'{temp_dir}explanations.json', 'w') as file:
            json.dump(explanations, file, indent=4)
    return explanations


async def generate_images(
    explanations: list[dict],
    title: str,
    subtitle: str,
    project_dir: str
) -> list[np.ndarray]:
    images = []
    cover_image, dir_image = None, None
    for i, item in enumerate(explanations):
        if item['file_path'] == '' or item['file_path'] is None or item['file_path'] == '0':
            img = await asyncio.to_thread(
                draw_project_cover,
                project_title=title, project_subtitle=subtitle
            ) if not cover_image else cover_image
        elif item['file_path'] == './':
            img = await asyncio.to_thread(
                draw_project_tree,
                title, generate_codebase_tree(project_dir)
            ) if not dir_image else dir_image
        else:
            item['file_path'] = os.path.join(test_dir, item['file_path'])
            item['code'] = open(item['file_path'], 'r').read()
            if not item['start_line'] or item['start_line'] < 2:
                item['start_line'] = None
            try:
                img = await asyncio.to_thread(
                    create_screenshot,
                    code=item['code'],
                    file_rel_path=os.path.relpath(item['file_path'], test_dir),
                    highlight_start=item['start_line'],
                    highlight_num_lines=(item['end_line'] - item['start_line'] + 1) if item['start_line'] else None
                )
            except Exception as e:
                print(f'file {item["file_path"]} failed to generate screenshot: {e}')
                img = Image.new('RGB', (3524, 2068), color=(0, 0, 0))
        images.append(np.array(img))
        img.save(f'{temp_dir}{i}.png')
        print(f'Created screenshot for {i}.png')
    return images


async def generate_audios(explanations: list[dict], tts: SpeechTextConverter) -> tuple:
    audios = []
    for i, item in enumerate(explanations):
        # create audio
        sr, audio_np = await asyncio.to_thread(
            tts.str_to_audio,
            preprocess_text(item['explanatory_text'])
        )
        audios.append(audio_np)
        # save_audio_to_file(audio_np, sr, f'{temp_dir}{i}.mp3')
        print(f'Created audio for {i}.mp3')
    return audios, sr


async def main() -> None:
    project_title = input("Enter project title: ")
    project_subtitle = input("Enter project subtitle: ")
    tts = SpeechTextConverter()
    explanations = get_explanations(project_title)
    # Run image & audio generation concurrently
    images, (audios, sr) = await asyncio.gather(
        generate_images(explanations, project_title, project_subtitle, test_dir),
        generate_audios(explanations, tts),
    )
    # merge audios & images
    final_video = merge_all(audios, images, sr=sr)
    final_video.write_videofile(f'{temp_dir}final_video.mp4')


if __name__ == "__main__":
    asyncio.run(main())
