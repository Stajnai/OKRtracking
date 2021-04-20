from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import OKR_Analyze as okr
import cv2

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

browse = Button(frame1, text = "Browse From Computer", command = Browse, bg = "white")
browse.grid(row = 0, column = 1)


#Select Eye Num and Label
frame = LabelFrame(window, text =  "")
frame.grid(row = 1, column = 0, sticky = 'w')
eyeNum = 0
eyeNumLabel = Label(frame, text = "Select which eye to Analyze:")
eyeNumDesc = Label(frame, text = "Both", width = 8, bg = "yellow" )

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

left = Button(frame, text = "Left", command = Left, padx = 12)
both = Button(frame, text = "Both", command = Both, padx = 10)
right = Button(frame, text = "Right", command = Right, padx = 8)

eyeNumLabel.grid(row = 0, column = 0, sticky = 'w')
eyeNumDesc.grid(row = 0, column = 1,sticky = 'w')
left.grid(row = 0, column = 2,sticky = 'w')
both.grid(row = 0, column = 3,sticky = 'w')
right.grid(row = 0, column = 4,sticky = 'w')

#Go Button
def Go():
	proj = okr.Project(filepath)
	cv2.imshow("Fish", proj.frame)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
go = Button(window, text = "Select\nData\nFirst", bg = "gray", height = 3, width = 5,command = Go, state = DISABLED)
go.grid(row = 0, column = 1, rowspan = 2)

#Welcome Image
welomeImg = ImageTk.PhotoImage(Image.open("GUI_Pics//StartUpFish.png"))
WelcomeImgShow = Label(window, image = welomeImg)
WelcomeImgShow.grid(row = 2, column = 0, columnspan = 6)

window.mainloop()