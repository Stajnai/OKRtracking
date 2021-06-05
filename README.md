# Optokinetic Response Tracking Software (Senior Thesis)
Written By: Sophia Tajnai\
Contact me with Questions: Sophia.Tajnai@gmail.com

## Purpose
#### Video Explanation: [https://www.youtube.com/watch?v=3OEmxjHBf3E]
  The Carthage College neuroscience department is taking part in research of the natural regenerative capabilities of the optical nerve in zebrafish, also known as *danio rerio*. As part of the study, a zebrafish's optical nerve is crushed and then the fish is observed as it regains vision. To test the capabilities of the eye, the optokinetic response (OKR) is recorded; this response is a natural reflex that stabilizes the eye during visual tracking (An example of this reflex can be seen here: [https://www.youtube.com/watch?v=LInm9cZcHyk]).The ocular angle formed by the axis of the eye and the long middle axis of the fish can be measured and graphed to show the OKR.\


The means of analysis for **adult** zebrafish at Carthage is manually analyzing each frame of the video. There is currently no open source software that provides analysis of the videos for adult zebrafish. (There is software available for the larval fish based on their lack of pigmentation but is not usable for adults.) This software helps semi-automate the analysis of the videos and reduces the time per video from ~8 hours of manual time to ~2.5 minutes via software.

## Specs (Language and Modules)
This software was written completely in Python 3. Modules used are:
* OpenCV (cv2)
* SciKit Skimage (Filter, Segmentation, Transform)
* NumPy
* MatPlotLib
* SciPy
* CSV
* Tkinter
* Pillow (PIL)

## How to Run
Install these three things:
Visual Studio Code: [https://code.visualstudio.com/download]
Python: [https://www.python.org/downloads/]
Pip Install: [https://pip.pypa.io/en/stable/installing/]

(This is assuming visual studio code, python 3, and pip install are already installed)
1. Clone this repository (download to zip file option then unzip).
2. Open in Visual Studio Code.
3. Make sure the files StartUpGUI and OKR_Analyze are in the same folder as well as the GUI_Pics folder containing StartUpFish (It is best to leave in original organization).
4. Have your .mp4 file of choice or the ExampleTrim file ready for use. (Currently the only vetted file type to use is .mp4 - Fiji software allows for file conversion)
5. Open a new terminal (In the upper ribbon called "Terminal" in Visual Studio Code)
6. Type in the terminal `python .\StartUpGUI.py` and press enter
7. If you do not have certain modules installed, it will tell you they need to be installed. It will give you the commands to type to install them (Something like "pip install opencv-python")
8. Once all of the relevant modules are installed, run the command `python .\StartUpGUI.py` again and follow the instructions on screen. (If two screens covering eachother, move them apart to see instructions in blue)
9. If you need to get out of the software at any point, press ctrl + c. **Note:** This will cancel everything and not finish the analysis process if it is still going.

