from tkinter import *
root = Tk()

def key(event):
    print(f'{event.keycode=}, {event.state=}, {hex(event.state)=}')

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()