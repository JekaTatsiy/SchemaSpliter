import sys

v = {a[0]: a[1] if len(a) == 2 else '' for a in [a.split('=')
                                                 for a in sys.argv[1:]]}

if len(v) == 0:
    v.append('-h')

method = v.get('-m')
if method is None:
    v.append('-h')

h = v.get('-h')
if h is not None:
    print('''
help msg
''')

if method is not None:
    if method == 'add':
        print('add')
