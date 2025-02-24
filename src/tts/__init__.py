import io
import numpy as np
from gtts import gTTS
import soundfile as sf


"""
This package is responsible for converting text to engaging audio using AI.
"""

import os
import io
import numpy as np
from datasets import load_dataset
from torch import tensor, float32
from transformers import pipeline


class SpeechTextConverter:
    def __init__(self):
        # Create text to speech pipeline with needed parameters
        synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
        # Get speaker embeddings, it is necessary to pass this for the model with the forward params
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embedding = tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        self.tts_pipe = lambda text: synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})

    def str_to_audio(self, text: str) -> tuple:
        # Convert text to speech using the model
        output = self.tts_pipe(text)
        audio_segment = output["audio"]
        sample_rate = output["sampling_rate"]

        # Return audio in the format gradio's Audio component needs
        return sample_rate, audio_segment


def preprocess_text(text: str) -> str:
    """This function is meant to improve the quality of the audio by reformatting the text"""
    characters_to_ignore = (',', '"', '`', '_', '-')
    for character in characters_to_ignore:
        text = text.replace(character, ' ')
    text = text.strip().lower()
    return text


def save_audio_to_file(audio_data: np.ndarray, sample_rate: int, file_path: str) -> None:
    sf.write(file_path, audio_data, sample_rate)


if __name__ == "__main__":
    TTS = SpeechTextConverter()
    sr, audio = TTS.str_to_audio("Alright, we're starting in `main.py`. This looks like the entry point of our script. It begins by importing necessary modules, `os` for file system operations and `generate_notebook` from `nb_generator` which sounds like the core functionality.")
    save_audio_to_file(audio, sr, "temp.mp3")
