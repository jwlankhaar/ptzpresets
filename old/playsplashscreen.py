
import tkinter.ttk as ttk

import ptzpresets.splashscreen as splashscreen

class View(ttk.Frame):
    def __init__(self):
        super().__init__()
        lbl = ttk.Label(self.master, text='Test')    
        lbl.pack(padx=50, pady=50)

class Contr:
        spl = splashscreen.Splashscreen(master=self.master)
        spl.build_view()
        spl.statusbar.inform('Connecting to cameras...')
    
        


# class contr:
#     f = ttk.Frame()
#     lbl = ttk.Label(master=f, text='Dit is een test')
#     lbl.pack(padx=50, pady=50)

#     view = splashscreen.View()
#     view.build_view()
#     view.statusbar.inform('Connecting to cameras...')
#     # view.mainloop()

v = View()
v.mainloop()
