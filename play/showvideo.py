from collections import Counter
from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from typing import Tuple, TypeVar, Union, List
import cv2

from PIL import Image, ImageTk

Coordinate = Tuple[Union[int, float], Union[int, float]]

# cap = cv2.VideoCapture('RTSP://192.168.2.40/videodevice')
cap = cv2.VideoCapture(0)

def load_imagetk(file: Path) -> ImageTk:
    """Load an image from file and return a Tk-compatible image."""
    return ImageTk.PhotoImage(Image.open(file))

class Joystick:
    FINDER_IMG = Path('play/camera_control_outercircle_alpha.png')
    STICK_IMG = Path('play/camera_control_outercircle_alpha.png')
    
    def __init__(self, master: tk.Canvas, center_x: int, center_y: int):
        self.finder = load_imagetk(self.FINDER_IMG)
        self.stick = load_imagetk(self.STICK_IMG)
        self.center = (center_x, center_y)
        self.master = master
        self.finder_id = self.master.create_image(
            self.center, anchor=tk.CENTER,
            image=self.finder, 
            state=tk.HIDDEN
        )
        self.stick_id = self.master.create_image(
            self.center, anchor=tk.CENTER,
            image=self.stick, 
            state=tk.HIDDEN
        )
        self.master.bind('<Enter>', self._show)
        self.master.bind('<Leave>', self._hide)
    
    def _hide(self, event):
        self.master.itemcget(self.finder_id, state=tk.HIDDEN)
        self.master.itemcget(self.stick_id, state=tk.HIDDEN)
    
    def _show(self, event):
        self.master.itemconfig(self.finder_id, state=tk.NORMAL)
        self.master.itemconfig(self.stick_id, state=tk.NORMAL)
        
#     def _drag(self, event):
#         pass
    
#     def _drop(self, event):
#         pass
        
    
class StickFilter:
    """Class that mimicks a filter to the mouse pointer coordinates to
    mimick the joystick's inertia and resistance.
    """
    def __init__(self, center: Coordinate, max_radius_px: int):
        # set filter parameters
        pass
    
    #TODO: Use Bézier curves?
    
    def filter(self, coordinates) -> Coordinate:
        # apply filter
        # return filtered coordinates
        pass
    
    def _response_func(x):
        pass
        
    def __call__(self, coordinates):
        """Make the instance callable."""
        return self._filter(coordinates)
    
class CurveIsNotMonotonicFunctionError(Exception):
    pass
    
class CurveIsNotAFunctionError(Exception):
    pass
    
class CubicBezier:
    def __init__(self, p: Coordinate, q: Coordinate, n: int):
        self.p, self.q, self.n = p, q, n
                
    def is_monotonic_function(self) -> bool:
        """Check whether the Bézier curve can be a (weak) monotonic 
        function of the form y = f(x). 
        """
        curve = self._get_curve()
        _, y = zip(*sorted(curve, key=lambda c: c[0]))
        dy = [y2-y1 for y1, y2 in zip(y[:-1],y[1:])]
        if dy[0] >= 0:
            return all(d >= 0 for d in dy)
        else:
            return all(d <= 0 for d in dy)
        
    def is_function(self) -> bool:
        """Check whether the Bézier curve can be a function of the form
        y = f(x). Return false if multiple distinct y values are found
        for the same x value (vertical line test).
        """
        px, qx = self.p[0], self.q[0]
        coefficients = [None, 3*px, (-6*px + 3*qx), (3*px - 3*qx + 1)]       
        for x in np.linspace(0, 1, self.n):
            coefficients[0] = -x
            polyn = np.polynomial.Polynomial(coefficients, domain=(0,1))
            relevant_roots = [r for r in polyn.roots() 
                              if not np.iscomplex(r) and 0 <= r <= 1]
            if len(relevant_roots) > 1:
                return False
        return True
        
    def _get_curve(self):
        """Return the coordinates for t in [0, 1]."""
        t_ = [i/self.n for i in range(self.n)]
        return [(self.x_func(t), self.y_func(t)) for t in t_]

    def x_func(self, t):
        """Return the x-coordinate of the curve for parameter t."""
        px, qx = self.p[0], self.q[0]
        return 3*(1 - t)**2*t*px + 3*(1 - t)*t**2*qx + t**3
    
    def y_func(self, t):
        """Return the y-coordinate of the curve for parameter t."""
        py, qy = self.p[1], self.q[1]
        return 3*(1 - t)**2*t*py + 3*(1 - t)*t**2*qy + t**3
    
    def as_func(self, x: float) -> float:
        """Return the y value corresponding to x if the curve is
        regarded as a function y = f(x). Find the parameter t that
        corresponds to x and use it to calculate y.
        """
        if not self.is_function():
            raise CurveIsNotAFunctionError
        px, qx = self.p[0], self.q[0]
        coefficients = [-x, 3*px, (-6*px + 3*qx), (3*px - 3*qx + 1)]       
        polyn = np.polynomial.Polynomial(coefficients, domain=(0,1))
        t = polyn.roots()
        if len(t) > 1:
            raise CurveIsNotAFunctionError
        return self.y_func(t)

bFunction = CubicBezier((0.6, 0.05), (0.2,-0.7), 50)
bNotFunction = CubicBezier((1.6, 0.8), (0.2,-0.7), 50)
print(f'{bFunction.is_function()=}')
print(f'{bNotFunction.is_function()=}')
print(f'{bFunction.as_func(0.3)=}')

class MotionPlanner:
    """Class that translates joystick movements to camera 
    movements.
    """
    def __init__(self, center_x, center_y, r_max, filter_properties):
        pass
        # current_position
        # last_updated
    
    def _filter(self, x, y, t):
        # ax, ay, vx, vy?
        # apply filter function
        # apply filtered coordinates
        pass
    
    
        
        
        
        

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()
        self.stream_image_id = self.canvas.create_image(0, 0, anchor=tk.NW)
        self.coordinates_text = tk.StringVar(master=self.master, value='')
        self._build_camera_controls()
        self._joystick_position = {'x': 265, 'y': 200}
        self.show_frame()
        
    def _build_camera_controls(self):
        outer_img = Image.open('play/camera_control_outercircle_alpha.png')
        inner_img = Image.open('play/camera_control_innercircle_alpha.png')
        
        self.inner_img = ImageTk.PhotoImage(inner_img)
        self.outer_img = ImageTk.PhotoImage(outer_img)
        self.outer_image_id = self.canvas.create_image(
            (265, 200), 
            anchor=tk.CENTER, 
            image=self.outer_img, 
            state=tk.HIDDEN
        )
        self.inner_img_id = self.canvas.create_image(
            (265, 200), 
            anchor=tk.CENTER, 
            image=self.inner_img,
            disabledimage=None,
            activeimage=self.inner_img, 
            state=tk.HIDDEN
        )
        self.canvas.bind('<Enter>', self._toggle_control_visibility)
        self.canvas.bind('<Leave>', self._toggle_control_visibility)
        self.canvas.tag_bind(self.inner_img_id, '<B1-Motion>', 
                             self._drag_joystick_callback)
        self.canvas.tag_bind(self.inner_img_id, '<ButtonRelease-1>', 
                             self._drop_joystick_callback)
        self.coordinates_label = tk.Label(master=self.master, 
                                          textvariable=self.coordinates_text)
        self.coordinates_label.pack()
        
        
    def _toggle_control_visibility(self, event):
        if self.canvas.itemcget(self.outer_image_id, 'state') == tk.HIDDEN:
            self.canvas.itemconfig(self.outer_image_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.inner_img_id, state=tk.NORMAL)
        else:
            self.canvas.itemconfig(self.outer_image_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.inner_img_id, state=tk.HIDDEN)
        
    def _drag_joystick_callback(self, event):
        self.coordinates_text.set(f'{event.x}, {event.y}')
        delta_x = event.x - self._joystick_position['x']
        delta_y = event.y - self._joystick_position['y']
        self.canvas.move(self.inner_img_id, delta_x, delta_y)
        self._joystick_position['x'] = event.x
        self._joystick_position['y'] = event.y
        # https://stackoverflow.com/a/6789351
        
        # get mouse position
        # move image to mouse position
        # translate mouse position to camera route
        # move camera        
        
    def _drop_joystick_callback(self, event):
        delta_x = 265 - self._joystick_position['x']
        delta_y = 200 - self._joystick_position['y']
        self.canvas.move(self.inner_img_id, delta_x, delta_y)
        self._joystick_position['x'] = 265
        self._joystick_position['y'] = 200
        # R = 35
        # r = 20
        # c = self.canvas
        # c.create_oval(265-R, 200-R, 265+R, 200+R, outline='red', width=1) 
        # c.create_oval(265-r, 200-r, 265+r, 200+r, fill='red', width=0)
        
    def read_frame(self):
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            scale_factor = 400/h
            frame = cv2.resize(frame, (int(w*scale_factor), int(h*scale_factor)))
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
cv2.destroyAllWindows()

