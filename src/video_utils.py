import numpy as np
from moviepy.video.VideoClip import VideoClip
from moviepy.audio.AudioClip import AudioClip, AudioArrayClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


"""
This module is responsible for any actions related to videos
"""


def merge_audios(audios: list[np.ndarray], sr: int, silent_separator: float=0.5) -> AudioClip:
    # Create a silent separator (mono)
    num_samples = int(sr * silent_separator)
    silent_audio = np.zeros(num_samples, dtype=np.float32)
    # Merge audios with silence in between
    merged_audio = np.concatenate([clip for audio in audios for clip in (audio, silent_audio)])[:-num_samples]  # Remove final silence
    # Ensure it's in the correct shape for MoviePy (2D array with shape (num_samples, 1))
    merged_audio = merged_audio.reshape(-1, 1)
    # Create an AudioClip from the merged audio array
    # use 44100 coz it works :)
    full_audio = AudioArrayClip(merged_audio, fps=44100)
    return full_audio


def create_image_sequence(images: list[np.ndarray], durations: list[float]) -> ImageSequenceClip:
    return ImageSequenceClip(sequence=images, durations=durations)


def concat_video_audio(video: VideoClip, audio: AudioClip) -> VideoClip:
    return video.with_audio(audio)


def merge_all(audios: list[np.ndarray], images: list[np.ndarray], sr: int) -> VideoClip:
    full_audio = merge_audios(audios, sr=sr, silent_separator=0.5)
    images_durations = [(audio_np.shape[0] / sr) + 1.5 for audio_np in audios]
    images_video = create_image_sequence(images, images_durations)
    final_video = concat_video_audio(video=images_video, audio=full_audio)
    return final_video
