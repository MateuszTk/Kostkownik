from tkinter import *

#canvas parameters:
canvas_width = 800
canvas_height = 480

master = Tk()

canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()

submenu = 0

def menu1(): submenu = 0
def menu2(): submenu = 1
def menu3(): submenu = 2

def update(solveString):
	canvas.delete("all")
	
	m1Button = Button(master, text="Main", command=menu1)
	m1Button.place(x = 30, y = 15, width = 90, height = 30)
	
	m2Button = Button(master, text="Cameras", command=menu2)
	m2Button.place(x = 30, y = 55, width = 90, height = 30)
	
	m3Button = Button(master, text="Motors", command=menu3)
	m3Button.place(x = 30, y = 95, width = 90, height = 30)
	
	if submenu == 0:		#Main submenu
		sbutton = Button(master, text="Solve", command=test)
		sbutton.place(x = 700, y = 15, width = 90, height = 90)
		
		label = Label(master, text=solveString, anchor='w')
		label.place(x = 10, y = 460, width = 780, height = 20)

	elif submenu == 1:	#Camera submenu
		t2button = Button(master, text="Cameras", command=test)
		t2button.place(x = 700, y = 15, width = 90, height = 90)
		
	elif submenu == 2:	#Motor submenu
	
		t3button = Button(master, text="Motors", command=test)
		t3button.place(x = 700, y = 15, width = 90, height = 90)
	
	
def test():
	print("tescik")

