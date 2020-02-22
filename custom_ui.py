from tkinter import *


#canvas parameters:


canvas_width = 800
canvas_height = 480

master = Tk()

canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()
submenu = 0
_submenu = -1

def test():
	print("tescik")
def menu1():
	global submenu
	submenu = 0
def menu2(): 
	global submenu
	submenu = 1
def menu3(): 
	global submenu
	submenu = 2

solveString = 'solve string'
_solveString = ''

#global definition and placement
m1Button = Button(master, text="Main", command=menu1)
m1Button.place(x = 30, y = 15, width = 90, height = 30)

m2Button = Button(master, text="Cameras", command=menu2)
m2Button.place(x = 30, y = 55, width = 90, height = 30)

m3Button = Button(master, text="Motors", command=menu3)
m3Button.place(x = 30, y = 95, width = 90, height = 30)

# main definition
label = Label(master, text=solveString, anchor='w')
sbutton = Button(master, text="Solve", command=test)

# cameras definition
t2button = Button(master, text="Cameras", command=test)

			
# motors definition
t3button = Button(master, text="Motors", command=test)
		
def update(solveString):
	master.update_idletasks()
	master.update()
	
	global _submenu
	global _solveString
	global label
	
	if _submenu != submenu or _solveString != solveString:	
		sbutton.place_forget()
		label.place_forget()
		t2button.place_forget()
		t3button.place_forget()
		
		if submenu == 0:	#Main submenu
			sbutton.place(x = 700, y = 15, width = 90, height = 90)
			label = Label(master, text=solveString, anchor='w')
			label.place(x = 10, y = 460, width = 780, height = 20)

		elif submenu == 1:	#Camera submenu
			t2button.place(x = 700, y = 15, width = 90, height = 90)
			
		elif submenu == 2:	#Motor submenu
			t3button.pack()
			t3button.place(x = 700, y = 15, width = 90, height = 90)
			
		_submenu = submenu
		_solveString = solveString
	
	


