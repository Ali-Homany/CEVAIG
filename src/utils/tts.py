import numpy as np
import soundfile as sf
from kokoro import KPipeline


"""
This package is responsible for converting text to engaging audio using AI.
"""


class SpeechTextConverter:
    def __init__(self, speed: float=1.0):
        # create pipeline fot english tts
        self.pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
        # set voice
        self.voice = 'af_heart'
        self.speed = speed

    def str_to_audio(self, text: str) -> tuple:
        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=self.speed,
            split_pattern=None
        )
        for gs, ps, audio in generator:
            sr = 24000
            if audio is not None:
                return sr, audio
        raise Exception('Audio generation failed')


def preprocess_text(text: str) -> str:
    """This function is meant to improve the quality of the audio by reformatting the text"""
    characters_to_ignore = (',', '"', '`', '_', '-')
    for character in characters_to_ignore:
        text = text.replace(character, ' ')
    text = text.replace('.py', 'dot py')
    text = text.strip().lower()
    return text


def save_audio_to_file(audio_data: np.ndarray, sr: int, file_path: str) -> None:
    sf.write(file_path, audio_data, sr)


if __name__ == '__main__':
    tts = SpeechTextConverter()
    tts.str_to_audio('hello world')
