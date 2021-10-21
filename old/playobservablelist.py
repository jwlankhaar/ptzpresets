import dataclasses
import functools

import ptzpresets.observables as observables


def observer(a):
    print(f'List was changed and, by the way, {a=}')

q = observables.ObservableList()
q.append(1)
q.register_observer(
    functools.partial(observer, a=4)
)
q[0] = 3

d = dict()
d['a'] = observables.ObservableList()
d['b'] = observables.ObservableList()

@dataclasses.dataclass
class StateChange:
    event_type: str
    camera: str
    preset_token: str
    preset_name: str
    error_message: str

def d_observer():
    print(f'd was changed ({d.value=})')
    
d = observables.ObservableValue(None)
d.register_observer(d_observer)
d.value = 1


