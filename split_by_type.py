

import re
import os
import shutil
import sys

print(sys.argv)

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

types = set()
for b in blocks:
    types.add(b[2])

try:
    shutil.rmtree(folder)
except OSError as error:
    pass
finally:
    os.mkdir(folder)

for cmdType in types:
    path = os.path.join(folder, str(cmdType).replace(' ', ''))
    os.makedirs(path)

    for t in tables:
        added = 0
        f = open(os.path.join(path, t+".sql"), "x")

        correct = r'public\.'+t+r'(_.*seq|_.*idx|_.*key|_type)?;?\s'

        limit = len(blocks)
        iterator = 0

        while iterator < limit:
            if blocks[iterator][2] != cmdType:
                iterator = iterator+1
                continue

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
                    added = added+1
                    del blocks[iterator]
                    limit = limit-1
                    iterator = iterator-1
            iterator = iterator+1

        f.close()
        if added == 0:
            os.remove(os.path.join(path, t+".sql"))
    if len(os.listdir(path)) == 0:
        os.rmdir(path)


print("unused blocks:", len(blocks))

'''
f = open(os.path.join(folder, "unallocated.sql"), "x")
f.write(header[0])
for b in blocks:
    f.write(b[0])
f.write(tail[0])
'''

'''
def count_lines(folder, filename, chunk_size=1 << 13):
    with open(os.path.join(folder, filename)) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


cnts = sum([count_lines(folder, file) for file in os.listdir(folder)])
cnt = count_lines("", sqlFile)

print(cnts, cnt)
'''
