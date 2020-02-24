from tkinter import *


#canvas parameters:


c_width = 800
c_height = 436

master = Tk()

canvas = Canvas(master, width=c_width, height=c_height)
canvas.pack()
submenu = 0
_submenu = -1

_c_height = 0
_c_width = 0

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
m1Button.place(relx = 15 / 480, rely = 155 / 800, relwidth = 100 / 480, relheight = 50 / 800)

m2Button = Button(master, text="Cameras", command=menu2)
m2Button.place(relx = 15 / 480, rely = 215 / 800, relwidth = 100 / 480, relheight = 50 / 800)

m3Button = Button(master, text="Motors", command=menu3)
m3Button.place(relx = 15 / 480, rely = 275 / 800, relwidth = 100 / 480, relheight = 50 / 800)

windowOutline = canvas.create_rectangle(0 ,0, 1, 1, outline='red')

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
	
	c_height = master.winfo_height()
	c_width = master.winfo_width()
	
	canvas.config(width=c_width - 4, height=c_height - 4)
	
	global _submenu
	global _solveString
	global label
	global _c_width
	global _c_height
	
	global windowOutline
	
	if _submenu != submenu or _solveString != solveString or _c_width != c_width or _c_height != c_height:	
		sbutton.place_forget()
		label.place_forget()
		t2button.place_forget()
		t3button.place_forget()
		canvas.delete(windowOutline)
		
		windowOutline = canvas.create_rectangle(0 ,0, c_width, c_height, width = 20, outline='red')
		
		if submenu == 0:	#Main submenu
			sbutton.place(relx = 600 / 800, rely = 15 / 480, relwidth = 180 / 800, relheight = 180 / 480)
			
			label = Label(master, text=solveString, anchor='w', font=("TkDefaultFont", int(16 / 480 * c_height)))
			label.place(relx = 10 / 800, rely = 430 / 480, relwidth = 780 / 800, relheight = 30 / 480)

		elif submenu == 1:	#Camera submenu
			print('')
			
		elif submenu == 2:	#Motor submenu
			print('')
			
		_submenu = submenu
		_solveString = solveString
		_c_width = c_width
		_c_height = c_height

