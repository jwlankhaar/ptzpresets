import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox

from pathlib import Path

import ptzpresets.styles as styles


HELP_FILE = Path('ptzpresets') / 'help.txt'


def show_help():
    window = tk.Toplevel()
    window.title('PTZ Presets Help')
    help_txt = open(HELP_FILE, 'rt', encoding='utf8').read().replace('\\t', '\t')
    txt_widget = tk.Text(
        master=window, 
        font=styles.system_font(), 
        relief=tk.FLAT,
        background=window['background']
    )
    txt_widget.insert(index=tk.END, chars=help_txt)
    btn_ok = ttk.Button(master=window, text='OK', command=window.destroy)
    txt_widget.pack(padx=20)
    btn_ok.pack(pady=20)

app = ttk.Frame()
app.master.title('A sample')
btn = ttk.Button(text='help', command=show_help)
btn.pack(pady=20, padx=10)
app.mainloop()



# tkinter.showinfo