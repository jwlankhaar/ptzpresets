from tkinter import *

root = Tk()
root.geometry('250x150')

button1 = Button(text="TOP")
button1.pack(side = TOP, fill=BOTH, expand=True, padx=5, pady=5)

button2 = Button(text="Lef2")
button2.pack(side = TOP, fill=BOTH, expand=True, padx=5, pady=5)

button3 = Button(text="Top")
button3.pack(side = TOP)

button4 = Button(text="Bottom")
button4.pack(side = BOTTOM)

root.mainloop()