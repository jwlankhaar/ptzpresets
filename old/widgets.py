# coding: utf-8

"""
    Widget classes that serve as an interface to Tk.
"""

import tkinter as tk
import tkinter.ttk as ttk


class Button(ttk.Button):
    """Class that slightly extends the Ttk.Button widget class.

    Property:
    - enabled: Indicates whether the button is enabled.

    Methods:
    - enable(): Enable the button.
    - disable(): Disable the button.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__enabled = True

    @property
    def enabled(self): return self.__enabled

    def enable(self):
        """Change the button's state to enabled."""
        self.__enabled = True
        self['state'] = tk.NORMAL

    def disable(self):
        """Change the button's state to disabled."""
        self.__enabled = False
        self['state'] = tk.DISABLED


class Label(ttk.Label):
    """Class that slightly extends the Ttk.Label widget class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, text):
        """Update the text of the label widget."""
        self['text'] = text


class Treeview(ttk.Treeview):
    """
    Class that extends the Ttk.Treeview widget.

    Arguments:

    - parent: the treeview's parent frame.

    Methods:

    - setup(): Define columns and headings and select event.
    - insert(): Insert items into the tree.
    - update(): Update all items in the tree.
    - clear(): Remove all items from the tree.
    - get_selected_root_children(): Get selected items in the root.
    
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(master=parent, **kwargs)

    def setup(self, columns, columnwidths, headings, command):
        """Configure the treeview widget. Define its columns (in
        addition to the default column '#0'), set their widths and
        headings. Bind event handler command to the the 
        <<TreeviewSelect>> event.
        """
        self['columns'] = columns
        columns.insert(0, '#0')
        for (c, w, h) in zip(columns, columnwidths, headings):
            self.column(c, width=w, anchor=tk.W)
            self.heading(c, text=h, anchor=tk.W)
        self.bind('<<TreeviewSelect>>', command)

    def insert(self, parent='', column_data=()):
        """Insert an item at the end of the tree (or of parent) and 
        return its id. If parent is an empty string, insert the item 
        as a child of the root node, otherwise insert it as a child of
        the specified item. The first element of column_data (a tuple) 
        is shown in the default column (#0) and the other elements in 
        the user-defined columns of the tree. 
        """
        if isinstance(column_data, str):  # Data for single column only if string.
            text = column_data
            values = ()
        else:
            if not parent:                  # Root node.
                text = column_data[0]
                values = column_data[1:]
            else:                           # Non-root node
                text = ''
                values = column_data
        return super().insert(parent, 'end', text=text, values=values)

    def update(self, tree_data):
        """Replace the data in the tree with the items in tree_data,
        which is a list of tuples of the form [(parent, children)]. 
        children is a list of tuples with column data.
        """
        self.clear()
        for parent, children in tree_data:
            parent_id = self.insert(column_data=parent)
            for child_data in children:
                self.insert(parent=parent_id, column_data=child_data)

    def select(self, item_ids):
        """Add the item_ids to the current selection."""
        self.selection_add(item_ids)

    def get_selected_children(self, parent=''):
        """Return a list of ids of the items selected in the treeview.
        Return children of the specified parent only.
        """
        ids = []
        root_node_children = self.get_children(parent)
        for id in self.selection():
            if id in root_node_children:
                ids.append(id)
        return ids

    def clear(self):
        """Remove root element and all its children from the treeview."""
        self.delete(*self.get_children())


class Statusbar(Label):
    """
        Class that adds a status bar to the current frame.

        Methods:
        - update(): Set the status bar text.
        - alert(): Show a status bar text temporarily.
        - clear(): Remove the status bar text.

        Property:
        - text: the status bar text.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self['background'] = 'white'
        self.place(
            relx=0, 
            rely=1.0, 
            x=0, 
            y=0, 
            relwidth=1.0, 
            anchor=tk.SW
        )
        self.__text = ''
        pass

    @property
    def text(self): return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        super().update(
            text=f'  {value}'
        )

    def update(self, message):
        self.text = message
        self.after(100, self.update_idletasks())

    def alert(self, message, duration_seconds=0.5):
        """Show a message for a short period of time and reset the
        status bar text to its original text.
        """
        current_text = self.text
        self.update(message)
        self.after(int(duration_seconds*1000), self.update_idletasks())
        # import time
        # time.sleep(duration_seconds)
        # self.update_idletasks()
        # self.after(int(duration_seconds*1000), self.update_idletasks())
        self.update(current_text)


    def clear(self):
        self.update(message='')


