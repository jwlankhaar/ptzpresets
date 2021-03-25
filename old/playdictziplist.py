

d = {
    'p1': {'Name': 'Preset 1'}, 
    'p2': {'Name': 'Preset 2'}
}
b = [0, 1]

for token, button in zip(d, b):
    d[token]['button'] = button

print(d)
