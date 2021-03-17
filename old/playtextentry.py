import tkinter as tk

def trigger_rename(button):
    entry_text = tk.StringVar(master=button, value='Jomina')
    entry = tk.Entry(master=button, exportselection=False, textvariable=entry_text)
    entry.bind('<FocusIn>', lambda e: e.widget.select_range(start=0, end=tk.END))
    entry.bind('<Return>', lambda e: rename(e.widget))
    entry.bind('<Escape>', lambda e: e.widget.destroy)
    entry.pack(expand=tk.YES, fill=None, side=tk.TOP, anchor=tk.CENTER)
    entry.focus()

def rename(entry):
    print(entry.get())
    entry.destroy()


app = tk.Tk()
btn = tk.Button(master=app, text='Button')
btn.bind('<Control-Button-1>', lambda e: trigger_rename(button=e.widget))
btn.pack(padx=50, pady=50)
btn2 = tk.Button(master=app, text='Rename', command=lambda b=btn: trigger_rename(b))
btn2.pack(padx=50, pady=50)
app.mainloop()


