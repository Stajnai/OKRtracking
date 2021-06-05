from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import cv2

import OKR_Analyze as okr

# Create a tkinter window
window = Tk()
window.title("OKR Analyze")

#Welcome Label
frame1 = LabelFrame(window, text = '')
frame1.grid(row = 0, column = 0, sticky = 'w')
welcome = Label(frame1, text = "Please select a video with a *.mp4 extension:")
welcome.grid(row = 0, column = 0)

#Browse button
filepath = "" #this is for initial once Go is pressed
def Browse():
	global filepath
	filepath = filedialog.askopenfilename(initialdir = "/", title = "Select A File", filetypes = (("mp4 files","*.mp4"), ("all files", "*.*")))
	go.config(text = "Go", bg = 'green',state = NORMAL)

	fileName = filepath[ filepath.rfind('/')+1:len(filepath) ]
	pathLabel.config(text = fileName, bg = 'gainsboro')

browse = Button(frame1, text = "Browse From Computer", command = Browse, bg = "white")
browse.grid(row = 0, column = 1)


#Select Eye Num and Label
frame2 = LabelFrame(window, text =  "")
frame2.grid(row = 1, column = 0, sticky = 'w')
eyeNum = 0
eyeNumLabel = Label(frame2, text = "Select which eye to Analyze:")
eyeNumDesc = Label(frame2, text = "Both", width = 8, bg = "yellow" )

def Left():
	global eyeNum 
	eyeNum = -1
	eyeNumDesc.config(text = "Left")
def Both():
	global eyeNum 
	eyeNum = 0
	eyeNumDesc.config(text = "Both")
def Right():
	global eyeNum 
	eyeNum = 1
	eyeNumDesc.config(text = "Right")

left = Button(frame2, text = "Left", command = Left, padx = 12)
both = Button(frame2, text = "Both", command = Both, padx = 10)
right = Button(frame2, text = "Right", command = Right, padx = 8)

eyeNumLabel.grid(row = 0, column = 0, sticky = 'w')
eyeNumDesc.grid(row = 0, column = 1,sticky = 'w')
left.grid(row = 0, column = 2,sticky = 'w')
both.grid(row = 0, column = 3,sticky = 'w')
right.grid(row = 0, column = 4,sticky = 'w')

#Path Label Showing
pathLabel = Label(window, text = "No file selected...", width = 60, bg = "salmon")
pathLabel.grid(row = 2, column = 0, columnspan = 2)


#Welcome Image
welomeImg = ImageTk.PhotoImage(Image.open("GUI_Pics//StartUpFish.png"))
WelcomeImgShow = Label(window, image = welomeImg)
WelcomeImgShow.grid(row = 3, column = 0, columnspan = 6)

#Go Button
def Go():
	global eyeNum
	proj = okr.Project(filepath)

	browse.config(state = DISABLED)
	left.config(state = DISABLED)
	both.config(state = DISABLED)
	right.config(state = DISABLED)
	go.config(state = DISABLED)
	
	WelcomeImgShow.destroy()

	window.update()

	proj.setEyeNum(eyeNum)
	proj.findFishNose()
	
	text1 = "Click and drag to draw a rectangle around just the eyes.\nPress the SPACE button to confirm the ROI!"
	roiInstructions = Label(window, text = text1, bg = "light blue", width = 60 )
	roiInstructions.grid(row = 3, column = 0, columnspan = 2)
	window.update()

	while (proj.roi1 == None or proj.roi2 == (0,0)):
		proj.setROI()

	cv2.destroyAllWindows() 
	roiInstructions.destroy()

	text2 = "Set the Max and Min values by dragging the trackbars until satisfied.\nPress the SPACE button to confirm the values!"
	edgeInstructions = Label(window, text = text2, bg = 'light blue',width = 60)
	edgeInstructions.grid(row = 3, column = 0, columnspan = 2)

	window.update()

	while proj.min == 0 and proj.max == 0: # I'm concerned about this boolean not checking both???????????????????????????????????
		print("Please set the edge detection max and min values")
		proj.EdgeDetec()
	
	window.destroy()
	cv2.destroyAllWindows()

	proj.autoAnalyzeVideo()


	
go = Button(window, text = "Select\nData\nFirst", bg = "gray", height = 3, width = 5,command = Go, state = DISABLED)
go.grid(row = 0, column = 1, rowspan = 2)

window.mainloop()