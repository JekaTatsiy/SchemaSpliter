import os
import re
from time import sleep

sqlFile = "schema.sql"
folder = "./tables"


def count_lines(folder, filename, chunk_size=1 << 13):
    with open(os.path.join(folder, filename)) as file:
        return sum(chunk.count('--')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


cnts = sum([count_lines(folder, file) for file in os.listdir(folder)])
cnt = count_lines("", sqlFile)
print("count '--': ", cnt, cnts, "diff:", cnt-cnts)

textOne = open(sqlFile).read()

textGen = "".join([open(os.path.join(folder, filename)).read()
                  for filename in os.listdir(folder)])

spaceTextOne = re.sub('[ \n]', '', textOne)
spaceTextGen = re.sub('[ \n]', '', textGen)
print("count rows: ", len(spaceTextOne), len(spaceTextGen),
      "diff:", len(spaceTextOne)-len(spaceTextGen))



if len(spaceTextOne)!=len(spaceTextGen):
    one = textOne.split('\n')
    gen = textGen.split('\n')

    limone = len(one)
    limgen = len(gen)

    ione = 0
    while ione < limone:
        igen = 0
        while igen < limgen:
            if one[ione] == gen[igen]:
                del one[ione]
                del gen[igen]
                ione = (ione-1 if ione > 0 else 0)

                igen = 0
                limone = len(one)
                limgen = len(gen)
            igen = igen+1
        print('ione up', ione, '/', limone)
        ione = ione+1
        if ione > 7:
            break

    [print(x) for x in one[0:7]]
