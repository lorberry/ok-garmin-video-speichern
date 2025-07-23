# ok-garmin-video-speichern

## this program presses the F10 key as soon as you say “okay garmin, video speichern”, and this is how you use it:

1. run ```pip install -r requirements.txt```

2. download the model "```vosk-model-de-0.21```" from https://alphacephei.com/vosk/models, and put the extracted folder into the project directory

3. in a recording program of your choice, e.g. OBS, set the replay hotkey for saving a video with the replay buffer to F10

4. start the python program and wait for the model to load. then say “okay garmin” and wait for the beep sound. after the beep you have 5 seconds to say “video speichern” and if you do, the program will trigger F10 and the final beeping sound will play.

### why?
this repo serves as a fun project, and refers to this meme here:
https://www.youtube.com/watch?v=3q_p1aW6rLg

### big thanks
to jirmjahu for coming up with this very sigma idea!
