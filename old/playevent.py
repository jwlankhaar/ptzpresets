import tkinter as tk


def callback(event):
    pass

app=tk.Tk()
btn = tk.Button(master=app, text='Button')
btn.bind('<Button-1>', callback)
btn.pack(padx=50, pady=50)
app.mainloop()



