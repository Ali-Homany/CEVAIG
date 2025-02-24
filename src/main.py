import os
import json
from screenshotter.image_creator import create_screenshot, crop_code_image
from tts import SpeechTextConverter, save_audio_to_file, preprocess_text
from video_utils import create_video, merge_videos
from explainer import explain_codebase


temp_dir = './temp/'
test_dir = './testing/sample_code/'


explanations = explain_codebase(test_dir)
print(type(explanations), type(explanations[0]))
with open('./temp.json', 'w') as file:
    json.dump(explanations, file)


TTS = SpeechTextConverter()
short_time_seperator = 0.5
for i, item in enumerate(explanations):
    # create screenshot
    item['file_path'] = test_dir + item['file_path']
    item['code'] = open(item['file_path'], 'r').read()
    img = create_screenshot(item['code'], item['line'])
    img = crop_code_image(img, highlight_start=item['line'], total_lines=item['code'].count('\n'), max_lines_around=25)
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
videos = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.mp4')]
merge_videos(*videos)

print('Done!')
