#coding: utf-8

"""MVC tk example
https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017
"""


import tkinter as tk


class Observable:
    def __init__(self, inital_value=None):
        self._value = inital_value
        self.callbacks = []

    def add_callback(self, func):
        self.callbacks.append(func)

    def del_callback(self, func):
        del self.callbacks[func]

    def _run_callbacks(self):
        for func in self.callbacks:
            func(self._value)
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._run_callbacks()

    @value.deleter
    def value(self):
        del self._value
    

class Model:
    def __init__(self):
        self.my_balance = Observable(0)

    def add_amount(self, amount):
        self.my_balance.value += amount

    def withdraw_amount(self, amount):
        self.my_balance.value -= amount


class MainView(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(text='Account balance')
        self.label.pack(side='left')
        self.amount_control = tk.Entry(width=8)
        self.set_amount(0)
        self.amount_control.pack(side='left')
    
    def set_amount(self, amount):
        self.amount_control.delete(0, 'end')
        self.amount_control.insert('end', str(amount))

    
class AdjustView(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        self.add_button = tk.Button(text='Add', width=8)
        self.add_button.pack(side='left')
        self.withdraw_button = tk.Button(text='Withdraw', width=8)
        self.withdraw_button.pack(side='left')


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.my_balance.add_callback(self.money_changed)
        self.main_view = MainView(root)
        self.adjust_view = AdjustView(self.main_view)
        self.adjust_view.add_button.config(command=self.add_money)
        self.adjust_view.withdraw_button.config(command=self.withdraw_money)
        self.money_changed(self.model.my_balance.value)

    def add_money(self):
        self.model.add_amount(10)

    def withdraw_money(self):
        self.model.withdraw_amount(10)

    def money_changed(self, amount):
        self.main_view.set_amount(amount)
    

if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()



        




