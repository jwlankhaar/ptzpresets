import tkinter as tk

import ptzpresets.multibutton as multibutton

def process_preset_click(event):
        button = event.widget
        state = event.state_decoded
        if state == '<Button-1>':
            print('Test')
        elif state == '<Control-Button-1>':
            new_name = button.rename()
            print(new_name)
        elif state == '<Shift-Button-1>':
            button.rename(new_name='Plug een naam')
        elif state == '<Alt_L-Button-1>':
            button.playdown()

app = tk.Tk()

import ptzpresets.styles as styles
btn1 = multibutton.MultiButton(
    master=app, 
    text='Button1', 
    number=1, 
    callback=process_preset_click, 
    highlight_style='Highlighted.PresetButton.TButton',
    default_style='PresetButton.TButton'
)
btn2 = multibutton.MultiButton(
    master=app, 
    text='Button2', 
    number=2, 
    callback=process_preset_click, 
    highlight_style='Highlighted.PresetButton.TButton',
    default_style='PresetButton.TButton'
)
btn1.pack(padx=50, pady=50)
btn2.pack(padx=50, pady=50)
app.mainloop()