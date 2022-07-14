import re
import os

folder = "./tables"
m = open("migrations/migrations.txt").read()

files = m.splitlines()

tables = []
for f in files:
    f_time = f.split('_')[0]
    d = open(os.path.join('migrations', f)).read()
    t = re.findall(r'create table( if not exists)? ([\w\.\"]+)', d, re.I)
    for x in t:
        tables.append((f_time, x[1].replace('\"', '').split('.')[-1]))

tables.sort()
listdir = os.listdir(folder)
for t in tables:
    for l in listdir:
        if t[1] == l.split('.')[0]:
            try:
                os.rename(os.path.join(folder, l),
                          os.path.join(folder, t[0]+'_'+l))
            except:
                pass
