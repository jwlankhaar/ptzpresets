import tkinter as tk
from tkinter.constants import HIDDEN
import tkinter.ttk as ttk
import cv2

from PIL import Image, ImageTk

from pathlib import Path

# cap = cv2.VideoCapture('RTSP://192.168.2.40/videodevice')
cap = cv2.VideoCapture(1)


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()
        self.stream_image_id = self.canvas.create_image(0, 0, anchor=tk.NW)
        self._build_camera_controls()
        self.show_frame()
        
    def _build_camera_controls(self):
        outer_img = Image.open('play/camera_control_outercircle_alpha.png')
        inner_img = Image.open('play/camera_control_innercircle_alpha.png')
        
        self.inner_img = ImageTk.PhotoImage(inner_img)
        self.outer_img = ImageTk.PhotoImage(outer_img)
        self.inner_img_id = self.canvas.create_image(
            (265, 200), 
            anchor=tk.CENTER, 
            image=self.inner_img,
            disabledimage=None,
            activeimage=self.inner_img, 
            state=tk.HIDDEN
        )
        self.outer_image_id = self.canvas.create_image(
            (265, 200), 
            anchor=tk.CENTER, 
            image=self.outer_img, 
            state=tk.HIDDEN
        )
        self.canvas.bind('<Enter>', self._toggle_control_visibility)
        self.canvas.bind('<Leave>', self._toggle_control_visibility)
        
    def _toggle_control_visibility(self, event):
        if self.canvas.itemcget(self.outer_image_id, 'state') == tk.HIDDEN:
            self.canvas.itemconfig(self.outer_image_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.inner_img_id, state=tk.NORMAL)
        else:
            self.canvas.itemconfig(self.outer_image_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.inner_img_id, state=tk.HIDDEN)
        
        # R = 35
        # r = 20
        # c = self.canvas
        # c.create_oval(265-R, 200-R, 265+R, 200+R, outline='red', width=1) 
        # c.create_oval(265-r, 200-r, 265+r, 200+r, fill='red', width=0)
        
    def read_frame(self):
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        scale_factor = 400/h
        frame = cv2.resize(frame, (int(w*scale_factor), int(h*scale_factor)))
        if ret:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            return ImageTk.PhotoImage(image)
        else:
            return None
        
    def show_frame(self):
        self.current_frame = self.read_frame()
        if self.current_frame is not None:
            self.canvas.itemconfig(self.stream_image_id, image=self.current_frame)
            self.canvas.after(int(1000/25), self.show_frame)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
    cap.release()





# while True:

#     #print('About to start the Read command')
#     ret, frame = cap.read()
#     #print('About to show frame of Video.')
#     # cv2.imshow("Capturing",frame)
#     #print('Running..')
    
    

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

cap.release()
# cv2.destroyAllWindows()

