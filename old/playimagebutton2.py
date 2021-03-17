import tkinter as tk
import tkinter.ttk as ttk


IMG_DEFAULT = './static/button_add_preset_default.png'
IMG_HOVER = './static/button_add_preset_hover.png'

class Application(tk.Tk):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('RIGHT!')
        self.img_default = tk.PhotoImage(file=IMG_DEFAULT)
        self.img_hover = tk.PhotoImage(file=IMG_HOVER)
        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self):
        button1 = ttk.Label(image=self.img_default)
        button1.bind('<Button-1>', lambda e: print(f'Button 1'))
        button1.bind('<Enter>', lambda e: button1.config(image=self.img_hover))
        button1.bind('<Leave>', lambda e: button1.config(image=self.img_default))

        button2 = ttk.Label(image=self.img_default)
        button2.bind('<Button-1>', lambda e: print(f'Button 2'))
        button2.bind('<Enter>', lambda e: button2.config(image=self.img_hover))
        button2.bind('<Leave>', lambda e: button2.config(image=self.img_default))

        self.buttons = [button1, button2]

    def pack_widgets(self):
        for button in self.buttons:
            button.pack(padx=100, pady=10)

app = Application()
app.mainloop()




# image_default = tk.PhotoImage(file='default.png')
# image_hover = tk.PhotoImage(file='hover.png')

# btns = []
# for i in range(3):
#     btn = ttk.Label(master=app, image=image_default)
#     btn.bind('<Button-1>', lambda e: print(f'Button {i}'))
#     btn.bind('<Enter>', lambda e: btn.config(image=image_hover))
#     btn.bind('<Leave>', lambda e: btn.config(image=image_default))
#     btns.append(btn)

# for i, b in enumerate(btns):
#     b.grid(pady=15, padx=20)
# app.pack()

# app.mainloop()