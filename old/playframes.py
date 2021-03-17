#coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk





root = tk.Tk()

s = ttk.Style()
s.configure('TFrame', relief=tk.SUNKEN)
s.configure('SmallText.TLabel', font=('Segoe UI', 7))

frm_body = ttk.Frame(master=root)
lbl = ttk.Label(master=frm_body, text='Text on grid', anchor=tk.W)
lbl.grid(padx=5, pady=15)
frm_body.pack(expand=tk.YES, fill=tk.X)

frm_footer = ttk.Frame(master=root)
# dummy_lbl = ttk.Label(master=frm_footer, text='')
# dummy_lbl.grid()
sbr = ttk.Label(master=frm_footer, text='Statusbar text', anchor=tk.W, style='SmallText.TLabel')
# sbr.place(
#     relx=0,
#     rely=1,
#     relwidth=1,
#     anchor=tk.SW
# )
sbr.pack(expand=tk.YES, fill=tk.X)
frm_footer.pack(expand=tk.YES, fill=tk.X)

root.mainloop()


# btn = ttk.Button(master=frm_body, text='A button')

# frm_footer = ttk.Frame(master=root, style='Black.TFrame')
# # dummy_lbl = ttk.Label(master=frm_footer, anchor=tk.W)
# # print(f'Dummy label has height: {dummy_lbl.winfo_height()}')
# # frm_footer.config(height=dummy_lbl.winfo_height())


# # statusbar = ttk.Label(master=frm_footer, text='Statusbar')
# # statusbar['background'] = 'white'

# frm_body.grid(row=0)
# frm_footer.grid(row=1)
# # dummy_lbl.grid(sticky=tk.E+tk.W)
# # btn.grid(column=0, row=0, padx=15, pady=15)
# # statusbar.place(
# #     relx=0,
# #     rely=1,
# #     relwidth=1,
# #     anchor=tk.SW
# # )

# # sbr = ttk.Label(master=app_bottom, text='statusbar')
# # statusbar.place(
# #     relx=0,
# #     rely=1,
# #     relwidth=1,
# #     anchor=tk.SW
# # )
# # lbl.pack(side=tk.BOTTOM, fill=tk.X)
# # sbr.place(
# #     rely=1,
# #     relwidth=1,
# #     anchor=tk.SW
# # )
# # lbl['background'] = 'white'


# # btn.pack()
# # app_content = ttk.Frame(master=app)
# # app_statusbar = ttk.Frame(master=app)
# # btn = ttk.Button(master=app_content, text='A Button', command=None)
# # btn.grid(row=0, column=0, padx=15, pady=15,)
# # app_content.grid(row=0)

# # app_statusbar.grid(row=1)
# root.mainloop()