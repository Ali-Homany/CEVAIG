import os
import numpy as np
from PIL import Image
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.VideoClip import VideoClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
"""
This module is responsible for any actions related to videos
"""

def create_video(image: Image, audio_file_path: str, output_file_path: str, duration: int = None) -> VideoClip:
    """
    This method creates a video from an image and an audio file
    """
    # create video
    image = np.array(image)
    video = ImageClip(image, duration=duration or audio.duration)
    video.fps = 30
    # set audio
    audio = AudioFileClip(audio_file_path)
    video = video.with_audio(audio)
    # save
    video.write_videofile(output_file_path, codec='libx264', audio_codec='aac', fps=30, preset='ultrafast')
    return video


def merge_videos(*video_files: str) -> str:
    """
    This method merges multiple videos into a single video
    """
    command = 'ffmpeg -f concat -safe 0 -i videos.txt -c copy output.mp4'
    with open('videos.txt', 'w') as f:
        for video_file in video_files:
            f.write(f'file {video_file}\n')
    # run command
    os.system(command)
    # remove temp file
    os.remove('videos.txt')
    return 'output.mp4'
    # videos = [VideoFileClip(file).resized(height=720).with_fps(30) for file in video_files]
    # return concatenate_videoclips(videos, method='compose')
