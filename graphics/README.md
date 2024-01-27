# IRL


## input.txt
Your text input blackboard. Pranav's big AI model will write to this.
Format is [name, occupation, interests, x, y]

## picture_script.py
Turn text from input.txt into png. Reads from `input.txt` and uses font from `SouceSansPro-Semibold.tff`.

Then it applies a parabolic warp (mimicking a shader) so it will display properly in the AR headset. (Based on Project North Start shader reference: https://www.shadertoy.com/view/wsscD4#)

Then it updates an OpenCV video stream in a loop (as new images are generated to the same `output.png` location), which is displayed on the Project North Start Next (https://docs.projectnorthstar.org/project-north-star/northstar-next/assembly-guide) headset.


## SourceSansPro-Semibold.tff
The font, which `picture_script.txt` uses
