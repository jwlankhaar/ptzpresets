import tkinter as tk
import tkinter.ttk as ttk

from pathlib import Path

root = tk.Tk()

DND_POINTER_IMG = tk.PhotoImage(file=Path('static/drag_and_drop_pointer.png'))

window = ttk.Frame(master=root, width=400, height=400)
img = ttk.Label(master=window, image=DND_POINTER_IMG)
img.place(relx=0.5, rely=0.5)
# img.place(relx=0.5, rely=0.5)
# canvas = tk.Canvas(master=window, width=400, height=400)
# canvas.create_image(200, 200, image='static/drag_and_drop_pointer.png')
# canvas.pack()
window.pack(expand=True, fill=tk.BOTH)
root.mainloop()