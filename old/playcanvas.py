import tkinter as tk
import tkinter.ttk as ttk

from ptzpresets import widgets as ptzwidgets

root = tk.Tk()
root.geometry('200x300')

conf = {'width': 1.4, 'fill': 'blue'}

cursor_path = 'C:/Python-work/ptzpresets/static/drag_and_drop_cursor.cur'

root.config(cursor = '@'+cursor_path)

w = 100
h = 5
c = tk.Canvas(master=root, width=w, height=h)
c.create_line(0, 0, h/2, h/2, **conf)
c.create_line(0, h, h/2, h/2, **conf)
c.create_line(h/2, h/2, w - h/2, h/2, **conf)
c.create_line(w - h/2, h/2, w, 0, **conf)
c.create_line(w - h/2, h/2, w, h, **conf)
c.place(relx=0.1, rely=0.5)
root.mainloop()
