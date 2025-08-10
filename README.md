# CEVAIG
**Code Explanation-Video AI Generator**

AI-Powered program that creates a video about a given coding project, explaining it while doing a tour over its files.


## Tools Used
- Streamlit
- Ffmpeg
- Carbon
- Gemini API
- Kokoro TTS


## Components
The video generation process mainly consists of:

1- Generate explanations with highlights ([explainer](./src/utils/explainer/)):
- parse codebase
- generate explanations
- add highlighting

2- Convert each explanation into audio ([tts.py](./src/utils/tts.py))

3- Create image/screenshot for every explanation ([creator](./src/utils/creator/)):
- draw project cover
- draw project file structure tree
- create code screenshot-like for every explanation (depending on file & highlighting)

4- Merge audios + screenshots -> full video ([video_utils.py](./src/utils/video_utils.py)):
- merge audios into single audio
- create image sequence video (depending on audios length)
- merge audio + video

5- Combine all in one process ([core.py](./src/core.py))


## User Interface
Multi-step wizard is implemented using Streamlit at ([app.py](./src/app.py)), which guides the user through the following steps:
- Select project (local folder or github repo)
- Ignore some filetypes
- Specify num of explanations and voice speed
- Customize explanation style
- Edit & Confirm Explanations
- Generate video


## Usage
Assuming you have python>=3.10 installed, kindly follow the steps below to run the project locally:
- Install required python libraries:
```
pip install -r requirements.txt
```

- Install [carbon-new](https://www.npmjs.com/package/carbon-now-cli)

- Run [app.py](./src/app.py) using streamlit:
```
python -m streamlit run src/app.py
```

- Follow the steps to create your video

- Download it, enjoy it, share it!