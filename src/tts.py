import numpy as np
import soundfile as sf
from kokoro import KPipeline


"""
This package is responsible for converting text to engaging audio using AI.
"""


class SpeechTextConverter:
    def __init__(self):
        # create pipeline fot english tts
        self.pipeline = KPipeline(lang_code='a')
        # set voice
        self.voice = 'af_heart'

    def str_to_audio(self, text: str) -> tuple:
        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=1,
            split_pattern=None
        )
        for gs, ps, audio in generator:
            sr = 24000
            return sr, audio


def preprocess_text(text: str) -> str:
    """This function is meant to improve the quality of the audio by reformatting the text"""
    characters_to_ignore = (',', '"', '`', '_', '-')
    for character in characters_to_ignore:
        text = text.replace(character, ' ')
    text = text.replace('.py', 'dot py')
    text = text.strip().lower()
    return text


def save_audio_to_file(audio_data: np.ndarray, sample_rate: int, file_path: str) -> None:
    sf.write(file_path, audio_data, sample_rate)


if __name__ == "__main__":
    TTS = SpeechTextConverter()
    text = "Alright, we're starting in `main.py`. This looks like the entry point of our script. It begins by importing necessary modules, `os` for file system operations and `generate_notebook` from `nb_generator` which sounds like the core functionality."
    text = preprocess_text(text)
    sr, audio = TTS.str_to_audio(text)
    save_audio_to_file(audio, sr, "temp.mp3")
