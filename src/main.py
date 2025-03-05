import os
import json
import random
import asyncio
import numpy as np
from explainer import explain_codebase
from screenshotter import create_screenshot
from tts import SpeechTextConverter, preprocess_text, save_audio_to_file
from video_utils import (
    VideoClip,
    merge_audios,
    concat_video_audio,
    create_image_sequence,
)


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
        with open(f'{temp_dir}explanations.json', 'w') as file:
            json.dump(explanations, file)
    return explanations


def merge_all(audios: list[np.ndarray], images: list[np.ndarray], sr: int) -> VideoClip:
    full_audio = merge_audios(audios, sr=sr, silent_separator=0.5)
    images_durations = [round(audio_np.shape[0] / sr, 1) for audio_np in audios]
    images_video = create_image_sequence(images, images_durations)
    final_video = concat_video_audio(video=images_video, audio=full_audio)
    return final_video


async def generate_images(explanations: list[dict]) -> list[np.ndarray]:
    images = []
    for i, item in enumerate(explanations):
        item['file_path'] = test_dir + item['file_path']
        item['code'] = open(item['file_path'], 'r').read()
        if not item['start_line'] or item['start_line'] < 2:
            item['start_line'] = None
        img = await asyncio.to_thread(
            create_screenshot,
            code=item['code'],
            file_rel_path=os.path.relpath(item['file_path'], test_dir),
            highlight_start=item['start_line'],
            highlight_num_lines=(item['end_line'] - item['start_line'] + 1) if item['start_line'] else None
        )
        images.append(np.array(img))
        # img.save(f'{temp_dir}{i}.png')
        print(f'Created screenshot for {i}.png')
    return images


async def generate_audios(explanations: list[dict], tts: SpeechTextConverter) -> tuple[list[np.ndarray], int]:
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
    tts = SpeechTextConverter()
    explanations = get_explanations()
    # Run image & audio generation concurrently
    images, (audios, sr) = await asyncio.gather(
        generate_images(explanations),
        generate_audios(explanations, tts),
    )
    # merge audios & images
    final_video = merge_all(audios, images, sr=sr)
    final_video.write_videofile(f'{temp_dir}final_video.mp4')


if __name__ == "__main__":
    asyncio.run(main())
