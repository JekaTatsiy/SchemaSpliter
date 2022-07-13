from nis import maps
from operator import truediv
from pydoc import pathdirs
import re
import os
import shutil

sqlFile = "schema.sql"
folder = "./tables"

tables_set = set()
f = open(sqlFile)
text = f.read()
f.close()

header = re.findall(
    pattern=r'(--\n-- PostgreSQL database dump\n--\n[\w\s\n\.\(\)\{\}\'\"\+=;.,:-]+?)--\n',
    string=text,
    flags=re.M
)
tail = re.findall(
    pattern=r'(--\n-- PostgreSQL database dump complete\n--)',
    string=text,
    flags=re.M
)
blocks = re.findall(
    pattern=r'(--\n-- Name: ([\w\s]+); Type: ([\w\s]+); Schema: [\w\s-]+; Owner:[ \w\s-]+\n--([\w\s\n\.\(\)\{\}\[\]\'\"=;.,:]+))',
    string=text,
    flags=re.M)

print('block count', len(blocks))


tables = []
for b in blocks:
    if b[2] == 'TABLE':
        tables.append(b[1])

try:
    shutil.rmtree(folder)
except OSError as error:
    pass
finally:
    os.mkdir(folder)

for t in tables:
    f = open(os.path.join(folder, t+".sql"), "x")
    correct = r'public\.'+t+r'(_.*seq|_.*idx|_.*key|_type)?;?\s'
    limit = len(blocks)
    iterator = 0
    while iterator < limit:
        m = re.search(correct, blocks[iterator][3], re.M)
        if m is not None:
            write = False
            endIsNum = True

            try:
                int(blocks[iterator][1][-1])
            except:
                endIsNum = False

            if endIsNum:
                if t in blocks[iterator][1].split(" "):
                    write = True

            else:
                write = True

            if write:
                f.write(blocks[iterator][0])
                del blocks[iterator]
                limit = limit-1
                iterator = iterator-1
        iterator = iterator+1
    f.close()

print("unused blocks:", len(blocks))

f = open(os.path.join(folder, "unallocated.sql"), "x")
f.write(header[0])
for b in blocks:
    f.write(b[0])
f.write(tail[0])


def count_lines(folder, filename, chunk_size=1 << 13):
    with open(os.path.join(folder, filename)) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


cnts = sum([count_lines(folder, file) for file in os.listdir(folder)])
cnt = count_lines("", sqlFile)

print(cnts, cnt)
