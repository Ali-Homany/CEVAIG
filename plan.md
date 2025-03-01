## Envisioned Implementation Plan
~~1. codebase -> list[dict] explanations:~~  
   ~~1.1. parsing codebase in the best way~~  
   ~~1.2. creating good prompt~~  
   ~~1.3. requesting & parsing output~~  
~~2. explanations list[dict] -> video:~~  
   ~~2.1. explanations -> audio files (TTS)~~  
   ~~2.2. explanation -> file screenshot with highlight~~  
   ~~2.3. screenshot + duration + audio -> video clip (moviepy)~~  
   ~~2.4. merge video clips~~  


## Time Expectations
1.1: 1 hrs necessary + 3-4 hrs low priority  
1.2: 1-2 hrs low priority  
1.3: 2-4 hrs necessary  

2.1: 1-3 hrs medium priority  
2.2: 1 hr easy low priority  
2.3: 5-9 hrs highest priority  
2.4: 1-3 hrs medium priority  
2.5: 1-2 hrs easy low priority  

TOTAL (avg): 22 HRS

Time Buffer: 20% = 5 hrs

## Progress
Initial Version includes the whole process but basic quality, it just works. So we still need to improve parsing the codebase, find better TTS, improve the prompt, add transition clips...
Note that the plan was partially modified, for step 2 was simplified a bit, merging clips doesn't require timestamps or so on.

The Initial Version (all commits up to this) took around 8-9 hrs.

- Find & use a better TTS (kokoro) took about 1hr
- Search for best/easiest way to create beautiful screenshots, choose carbon-now-cli. Use it.
- Improve explainer, including prompt & Explanation structure (add end_line)

Version 2.0 (commits since Initial Version) took around 7-8 hrs.