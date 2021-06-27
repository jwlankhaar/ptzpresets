import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from math import inf
from pathlib import Path

def get_new_button_index(y):
    global snap_positions
    i = 0
    while i < len(snap_positions) - 1:
        if abs(y - snap_positions[i]) < 10:
            return i
        i += 1
    return i
    
def snap_filter(y):
    global snap_positions
    closest_snap_position = min(snap_positions, key=lambda p, y=y: abs(p - y))
    if abs(y - closest_snap_position) < 7:
        return closest_snap_position
    else:
        return y    

def callback(event=None):
    global pointer
    global button_positions
    # print(f'{event.x=}, {event.y=}')
    # print(get_new_button_index(event.y))
    pointer.place(relx=0.5, y=snap_filter(event.y), anchor=tk.CENTER)
    
def release_callback(event):
    global snap_positions
    try: 
        isnap = snap_positions.index(snap_filter(event.x))
    except ValueError:
        isnap = None
    if isnap is not None:
        print('snapped')
    else:
        print('not snapped')
    pointer.place_forget()  

root = ttk.Frame()
DND_POINTER_IMG = tk.PhotoImage(file=Path('static/drag_and_drop_pointer.png'))
pointer = ttk.Label(master=root, image=DND_POINTER_IMG)
btn1 = ttk.Button(master=root, text='Button 1')
btn1.bind('<B1-Motion>', callback)
btn1.bind('<ButtonRelease>', release_callback)
btn1.pack(padx=100, pady=20)

btn2 = ttk.Button(master=root, text='Button 2')
btn2.pack(padx=100, pady=20)

btn3 = ttk.Button(master=root, text='Button 3')
btn3.pack(padx=100, pady=20)
root.pack()
root.update()
button_positions = [
    0,
    btn1.winfo_y() + btn1.winfo_height()/2,
    btn2.winfo_y() + btn2.winfo_height()/2,
    btn3.winfo_y() + btn3.winfo_height()/2,
    root.winfo_height()
]
snap_positions = [(button_positions[i] + button_positions[i+1])/2 for i in range(len(button_positions)-1)]
print(f'{button_positions=}')

root.mainloop()