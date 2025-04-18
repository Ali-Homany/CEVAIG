import numpy as np
from moviepy.video.VideoClip import VideoClip
from moviepy.audio.AudioClip import AudioClip, AudioArrayClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


"""
This module is responsible for any actions related to videos
"""


def merge_audios(audios: list[np.ndarray], sr: int, silent_separator: float=0.5) -> AudioClip:
    # Merge audios with silence in between
    merged_audio = np.concatenate(audios)
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


def get_audio_length(audio_np: np.ndarray, sr: int) -> float:
    return (audio_np.shape[0] / sr) + 1.5


def merge_all(audios: list[np.ndarray], images: list[np.ndarray], sr: int) -> VideoClip:
    full_audio = merge_audios(audios, sr=sr, silent_separator=0.5)
    images_durations = [get_audio_length(audio_np, sr) for audio_np in audios]
    images_video = create_image_sequence(images, images_durations)
    final_video = concat_video_audio(video=images_video, audio=full_audio)
    return final_video


def save_video(video: VideoClip, output_path: str) -> None:
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
