import tkinter as tk
import tkinter.ttk as ttk


from ptzpresets import root

class W(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master.overrideredirect(True)
        self.master.eval(f'tk::PlaceWindow {str(self)} center')
        

f = W(master=root.root)
# root.root.overrideredirect(True)
# root.root.eval(f'tk::PlaceWindow {str(f)} center')
root.root.mainloop()