#coding: utf-8


"""Observable classes that implements a simple observable pattern.
"""

class ObservableMixin:
    """Mixin class that provides the functionality to 
    make a container class observable.
    """
    def register_observer(self, observer):
        if hasattr(self, 'observers'):
            self.observers.append(observer)
        else:
            self.observers = [observer]

    def _trigger_observers(self):
        if hasattr(self, 'observers'):
            for func in self.observers:
                func()

    def _decorate(self, func):
        """Retun a decorator that makes a method observable."""
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            self._trigger_observers()
            return value
        return wrapper

    def _make_observable(self, methods_to_decorate):
        """Decorate methods that change the container to make 
        them observable.
        """
        for attr in methods_to_decorate:
            setattr(self, attr, self._decorate(getattr(self, attr)))


class ObservableList(list, ObservableMixin):
    """Class that extends the list class with observer functionality.
    After registering an observer (a callable), the observer is 
    triggered each time the content of the list is changed.

    Parameters
    ----------
    Same as built-in list class.

    Methods
    -------
    register_observer(callable):
        Register a new observer in the list. Each observer
        will be called after the list content has changed.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        methods_to_decorate = [
            'append', 'clear', 'copy', 'extend', 'insert', 'pop', 'remove', 
            'reverse', 'sort'
        ]
        self._make_observable(methods_to_decorate)

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


class ObservableDict(dict, ObservableMixin):
    """Class that extends the dictionary class with observer 
    functionality. After registering an observer (a callable), 
    the observer is triggered each time the content of the
    dictionary is changed.

    Parameters
    ----------
    Same as built-in dictionary class.

    Methods
    -------
    register_observer(callable):
        Register a new observer in the dictionary. Each observer
        will be called after the dictionary content has changed.
    """    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        methods_to_decorate = [
            'clear', 'copy', 'pop', 'popitem', 
            'setdefault', 'update'
        ]
        self._make_observable(methods_to_decorate)

    # Magic methods have to be overloaded on class level.
    # https://stackoverflow.com/a/21990465/12646289
    def __delitem__(self, key):
        super().__delitem__(key)
        self._trigger_observers()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._trigger_observers()


class ObservableValue(ObservableMixin):
    """Class that defines a value with observer functionality. 
    After registering an observer (a callable), the observer
    will be triggered each time the value changes.
    
    Properties
    ----------
    value: property (get/set)
        The value to be observed.
        
    Methods
    -------
    register_observer(callable): 
        Register a new observer. Each observer will be called
        when the observable value has changed.
    """
    def __init__(self, value=None):
        self.__value = value

    @property
    def value(self): 
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self._trigger_observers()


