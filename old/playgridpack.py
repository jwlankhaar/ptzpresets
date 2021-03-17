import tkinter as tk
import tkinter.ttk as ttk

# root = tk.Tk()
# body = ttk.Frame(master=root)
# footer = ttk.Frame(master=root)
# lbl = ttk.Label(master=body, text='Test in body (grid)')
# lbl.grid()
# btn = ttk.Button(master=body, text='A button (grid)')
# btn.grid(row=0, column=1)
# sbr = ttk.Label(master=footer, text='Status (pack)')
# sbr.pack(expand=tk.YES, fill=tk.BOTH)
# body.pack(expand=tk.YES, fill=tk.BOTH)
# footer.pack(expand=tk.YES, fill=tk.BOTH)

# root.mainloop()


class Application(ttk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.create_frames()
        self.creat_widgets()
        self.position_frames()
        self.position_widgets()

    def create_frames(self):
        self.body = ttk.Frame(master=self.master)
        self.footer = ttk.Frame(master=self.master)

    def creat_widgets(self):
        self.body_lbl = ttk.Label(master=self.body, text='Test in body (grid)')
        self.btn = []
        for i in range(5):
            self.btn.append(ttk.Button(master=self.body, text=str(i)))
        self.footer_lbl = ttk.Label(master=self.footer, text='Text in footer (pack)')

    def position_frames(self):
        self.body.pack(expand=tk.YES, fill=tk.BOTH)
        self.footer.pack(expand=tk.YES, fill=tk.BOTH)

    def position_widgets(self):
        self.body_lbl.grid()
        for b in self.btn:
            b.grid()
        self.footer_lbl.pack(expand=tk.YES, fill=tk.BOTH)

root = tk.Tk()
app = Application(master=root)
root.mainloop()