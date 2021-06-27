import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsgbox

def callback(event=None):
    print('clicked')
    if event:
        print(event.widget.state())
        root.update_idletasks()


root = ttk.Frame()
btn1 = ttk.Button(master=root, text='Test1')
btn1.bind('<Button-1>', callback)
btn1.pack(padx=100, pady=20)
btn2 = ttk.Button(master=root, text='Test2', command=callback)
btn2.pack(padx=100, pady=20)
root.pack()
root.mainloop()