import os
import json
from screenshotter import create_screenshot
from tts import SpeechTextConverter, save_audio_to_file, preprocess_text
from video_utils import create_video, merge_videos
from explainer import explain_codebase


temp_dir = './temp/'
test_dir = './testing/sample_code/'


explanations = explain_codebase(test_dir)
with open('./temp.json', 'w') as file:
    json.dump(explanations, file, indent=4)


TTS = SpeechTextConverter()
short_time_seperator = 0.5
for i, item in enumerate(explanations):
    # create screenshot
    item['file_path'] = test_dir + item['file_path']
    item['code'] = open(item['file_path'], 'r').read()
    if not item['start_line'] or item['start_line'] < 2:
        item['start_line'] = None
    img = create_screenshot(
        code=item['code'],
        file_rel_path=os.path.relpath(item['file_path'], test_dir),
        highlight_start=item['start_line'],
        highlight_num_lines=(item['end_line'] - item['start_line'] + 1) if item['start_line'] else None
    )
    img.save(f'{temp_dir}{i}.png')
    print(f'Created screenshot for {i}.png')
    # create audio
    sr, audio_np = TTS.str_to_audio(preprocess_text(item['explanatory_text']))
    save_audio_to_file(audio_np, sr, f'{temp_dir}{i}.mp3')
    print(f'Created audio for {i}.mp3')
    # get audio metadata, length
    audio_length = audio_np.shape[0] / sr
    # create video
    video = create_video(img, f'{temp_dir}{i}.mp3', f'{temp_dir}{i}.mp4', duration=audio_length+short_time_seperator)
    print(f'Created video for {i}.mp4')
    # cleanup
    os.remove(f'{temp_dir}{i}.mp3')
    os.remove(f'{temp_dir}{i}.png')

# merge videos
videos = [
    os.path.join(temp_dir, f)
    for f in os.listdir(temp_dir)
    if f.endswith('.mp4')
]
videos.sort(key=lambda f: f.split('.')[0])
merge_videos(*videos)

print('Done!')
