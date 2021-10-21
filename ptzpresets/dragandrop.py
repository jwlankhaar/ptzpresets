"""
    Mixin class that enables drag and drop of widgets.
"""

import tkinter as tk

from ptzpresets import styles
    

class DragAndDropMixin:
    
    def dnd_init(self, master, widgets):
        self.dnd_grid = []
        self.snap_distance = styles.DRAGANDDROP_SNAP_DISTANCE
        self.pointer = styles.DRAGANDDROP_CURSOR
        self.widgets = widgets
        self._is_dragging = tk.BooleanVar(master, value=False)
        self._is_widgets_reordered = tk.BooleanVar(master, value=False)
        
    # Make is_dragging a property so that set and get don't 
    # have to be called explicitly.
    is_dragging = property(
        lambda self: self._is_dragging.get(), 
        lambda self, value: self._is_dragging.set(value)
    )
    
    is_widgets_reordered = property(
        lambda self: self._is_widgets_reordered.get(),
        lambda self, value: self._is_widgets_reordered.set(value)
    )

    def dnd_register_callbacks(self, widget):
        widget.bind('<B1-Motion>', self._drag_callback)
        widget.bind('<ButtonRelease-1>', self._drop_callback, add='+')
        
    def dnd_register_master_refresh_callback(self, callback):
        self.refresh_master = callback
       
    def _init_grid(self):
        """Initialize the drag and drop grid. The grid points are the 
        positions in the middle of the space between consecutive 
        widgets. 
        """
        # Get widget dimensions.
        H = self.widgets[0].master.winfo_height()       # parent height
        h = [w.winfo_height() for w in self.widgets]    # widget heights
        p = [w.winfo_y() for w in self.widgets]         # widget positions
        
        # Calculate the intermediate grid points first.
        g = [(p[i] + h[i] + p[i+1]) / 2 for i in range(len(p) - 1)]
        
        # The first and last point depend on adjacent (non-drag-and-drop) 
        # widgets (if any).
        w_first_dnd = self.widgets[0]
        siblings = w_first_dnd.master.winfo_children()
        siblings = sorted(siblings, key=lambda s:s.winfo_y())
        if siblings.index(w_first_dnd) > 0:
            i_before = siblings.index(w_first_dnd) - 1
            p_before = siblings[i_before].winfo_y()
            h_before = siblings[i_before].winfo_height()
            g.insert(0, (p_before + h_before + p[0]) / 2)
        else:
            g.insert(0, p[0]/2)
        
        w_last_dnd = self.widgets[-1]
        if siblings.index(w_last_dnd) < len(siblings) - 1:
           i_after = siblings.index(w_last_dnd) + 1
           p_after = siblings[i_after].winfo_y()
           g.append((p[-1] + h[-1] + p_after) / 2)
        else:
            g.append( (H + p[-1] + h[-1]) / 2)
          
        self.dnd_grid = g
        
    def _drag_callback(self, event=None):
        """Show drag and drop cursor. Apply snap filter."""
        self.is_dragging = True
        self._init_grid()   # Init here because widgets have been rendered
                            # and geometries are up to date.
        self._set_dnd_cursor()
        x = event.widget.master.winfo_width() / 2
        if self._is_snapping(self._y_relative(event)):
            # Move the mouse pointer.
            self.event_generate(
                '<Motion>', 
                warp=True, 
                x=x, 
                y=self._nearest_grid_point(self._y_relative(event))
            )
            # https://tcl.tk/man/tcl8.6/TkCmd/event.htm#M86
            # https://stackoverflow.com/a/16704353
        
    def _y_relative(self, event):
        return event.widget.winfo_pointery() - event.widget.master.winfo_rooty()

    def _drop_callback(self, event):
        """Reorder widgets if the current position is within a snap
        zone and hide drag and drop cursor.
        """
        self._reset_cursor()
        if self.is_dragging:
            y = self._y_relative(event)
            if self._is_snapping(y):
                widget_index = self.widgets.index(event.widget)
                g = self._nearest_grid_point(y)
                target_index = self.dnd_grid.index(g)
                self._reorder(widget_index, target_index)
            self.is_widgets_reordered = True
            self.is_dragging = False
        
    def _nearest_grid_point(self, y):
        """Return the position of the grid point closest to y.
        """
        return min(self.dnd_grid, key=lambda g, p=y: abs(g - p))
    
    def _is_snapping(self, y):
        """Return True if y is within snap distance of the grid.
        """
        return abs(y - self._nearest_grid_point(y)) < self.snap_distance
    
    def _grid_index(self, y):
        """Return the index of the grid point nearest to y if y is 
        within snap distance of the grid. Return None otherwise.
        """
        try:
            return self.dnd_grid.index(self.dnd_snap(y))
        except ValueError:
            return None
    
    def _reorder(self, widget_index, target_index):
        """Move the widget to the target index. 
        """
        if target_index <= widget_index:
            self.widgets.insert(target_index, self.widgets.pop(widget_index))
        elif target_index < len(self.widgets):
            widget = self.widgets.pop(widget_index)
            self.widgets.insert(target_index-1, widget)
        else:
            self.widgets.append(self.widgets.pop(widget_index))
        self._refresh()
            
    def _refresh(self):
        self._init_grid()
        self.refresh_master()
    
    def _set_dnd_cursor(self):
        self.config(cursor=styles.DRAGANDDROP_CURSOR)
        
    def _reset_cursor(self):
        self.config(cursor='')
