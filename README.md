# CEVAIG
**Code Explanation Video AI Generator**

AI-Powered program that creates a video about a given coding project, explaining it while doing a tour over its files.

## Components
The video generation process consists of 4 main steps:

1- Generate explanations with highlights ([explainer](./src/explainer/)):
- parse codebase
- generate explanations
- add highlighting

2- Convert each explanation into audio ([tts.py](./src/tts.py))

3- Create image/screenshot for every explanation ([creator](./src/creator/)):
- draw project cover
- draw project file structure tree
- create code screenshot-like for every explanation (depending on file & highlighting)

4- Merge audios + screenshots -> full video ([video_utils.py](./src/video_utils.py)):
- merge audios into single audio
- create image sequence video (depending on audios length)
- merge audio + video

## Usage
Currently this is still under development & testing, but you can try to use it for sure. (clone the latest 'Version X.X' commit).

Assuming you have python installed, kindly follow the steps below to run the project locally:
- Install required python libraries:
```
pip install -r requirements.txt
```

- Copy your project folder into [/testing/](./testing/) and rename it to `/sample_code`

- Run [main.py](./src/main.py)

- Find your video at `/temp/test_XXX/final_video.mp4`