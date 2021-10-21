from PIL import Image, ImageTk
import tkinter as tk




root = tk.Tk()

frame = tk.Frame(master=root,width=200, height=300)



canvas = tk.Canvas(master=frame)
canvas.create_line(50,50,200,50, width=1.5, tag='dnd_pointer')
canvas.create_line(45,45,50,50,45,55, width=1.5, capstyle=tk.ROUND, tag='dnd_pointer')
canvas.create_line(205,45,200,50,205,55, width=1.5, capstyle=tk.ROUND, tag='dnd_pointer')

frame.pack()
root.mainloop()