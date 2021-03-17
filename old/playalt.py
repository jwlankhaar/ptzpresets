import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

app = tk.Tk()
btn = ttk.Button(
    master=app, 
    text='Test', 
    command=lambda: messagebox.showinfo(message='Gewone KLIK!')
)
btn.bind('<Control-Button-1>', lambda e: messagebox.showinfo(message='Ctrl + KLIK!'))
btn.bind('<Alt-Button-1>', lambda e: messagebox.showinfo(message='Alt + KLIK!'))
btn.pack(padx=50, pady=50)
app.mainloop()