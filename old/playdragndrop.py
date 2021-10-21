import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from math import inf
from pathlib import Path

def get_new_button_index(y):
    global grid
    i = 0
    while i < len(grid) - 1:
        if abs(y - grid[i]) < 10:
            return i
        i += 1
        
    min(range(len(grid)), key=lambda i, y=y: abs(y - grid[i]))
    return i
    
def snap_filter(y):
    global grid
    closest_snap_position = min(grid, key=lambda p, y=y: abs(p - y))
    if abs(y - closest_snap_position) < 7:
        return closest_snap_position
    else:
        return y    

def drag_callback(event=None):
    global is_dragging
    global pointer
    global button_positions
    
    print('drag_callback')
    is_dragging.set(True)
    # print(f'{event.x=}, {event.y=}')
    # print(get_new_button_index(event.y))
    pointer.place(relx=0.5, y=snap_filter(event.y), anchor=tk.CENTER)
    
def drop_callback(event):
    global is_dragging
    global grid
    print('drop_callback')
    if is_dragging.get():
        print('is dragging')
        try: 
            isnap = grid.index(snap_filter(event.x))
        except ValueError:
            isnap = None
        # if isnap is not None:
        #     print('snapped')
        # else:
        #     print('not snapped')
        is_dragging.set(False)
        pointer.place_forget()
    else:
        print('is not dragging')
    
def click_callback(event=None):
    print('click callback')

root = ttk.Frame()
DND_POINTER_IMG = tk.PhotoImage(file=Path('static/drag_and_drop_pointer.png'))
pointer = ttk.Label(master=root, image=DND_POINTER_IMG)

is_dragging = tk.BooleanVar(master=root, value=False)

btn1 = ttk.Button(master=root, text='Button 1')
btn1.bind('<B1-Motion>', drag_callback)
# btn1.bind('<ButtonPress-1>', click_callback)
btn1.config(command=click_callback)
btn1.bind('<ButtonRelease>', drop_callback)
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
grid = [(button_positions[i] + button_positions[i+1])/2 for i in range(len(button_positions)-1)]
print(f'{button_positions=}')

root.mainloop()