import tkinter as tk
import tkinter.ttk as ttk


def toggle_highlight(event):
    btn = event.widget
    if btn['image']:
        btn.config(image=tk.PhotoImage(file='static\\empty_16x16.png'))
    else:
        btn.config(image=tk.PhotoImage(file='static\\current_preset.png'))

app = tk.Tk()
IMG = tk.PhotoImage(file='static\\current_preset.png')
import ptzpresets.styles as styles

styles.style.configure('MyButton.TButton.Label',
    foreground='red',
    background='black'
)
button = ttk.Button(master=app, text='MyButton', image=IMG, compound=tk.LEFT)
button.pack(padx=50, pady=50)
button.bind('<Button-1>', toggle_highlight)
app.mainloop()

