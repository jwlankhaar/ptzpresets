class ObservableList(list):
    def __init__(self, value):
        super().__init__(value)
        self.observers = []
        self._decorate_methods()

    def register_observer(self, callback):
        self.observers.append(callback)

    def _trigger_observers(self):
        for func in self.observers:
            func()

    def _make_observable(self, func):
        """Decorator that makes a method observable"""
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            self._trigger_observers()
            return value
        return wrapper

    def _decorate_methods(self):
        """Make methods that change the list observable 
        using the decorator
        """
        methods_to_decorate = [
            'append', 'clear', 'copy', 'extend', 'insert', 'pop', 'remove', 
            'reverse', 'sort'
        ]
        for attr in methods_to_decorate:
            setattr(self, attr, self._make_observable(getattr(self, attr)))

    # Magic methods have to be overloaded on class level.
    # https://stackoverflow.com/a/21990465/12646289
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._trigger_observers()

    def __reversed__(self):
        super().__reversed__()
        self._trigger_observers()

    def __delitem__(self, index):
        super().__delitem__(index)
        self._trigger_observers()



myd = dict()

pass