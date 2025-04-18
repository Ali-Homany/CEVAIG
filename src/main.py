import asyncio
from utils.video_utils import save_video
from utils.tts import SpeechTextConverter
from core import (
    get_explanations,
    generate_video,
    CACHE_DIR
)


def main() -> None:
    title = input("Enter project title: ")
    subtitle = input("Enter project subtitle: ")
    tts = SpeechTextConverter()
    explanations = get_explanations(title)
    # generate video
    final_video = generate_video(tts, explanations, title, subtitle)
    # save video
    save_video(final_video, f'{CACHE_DIR}{title}.mp4')


if __name__ == "__main__":
    main()
