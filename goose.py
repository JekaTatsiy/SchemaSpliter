# отсортировать миграции по времени их применения

from subprocess import PIPE, Popen
import subprocess
import os
import re
import shutil
import time
import datetime

migorig = 'migrations'
mig = 'migrationsCopy'

try:
    shutil.rmtree(mig)
except:
    pass

pg_host = 'localhost'
pg_user = 'postgres'
pg_password = 'postgres'
pg_dbname = 'asna'

dsn = ''
for A, B in zip(['user', 'password', 'dbname', 'sslmode'], [pg_user, pg_password, pg_dbname, 'disable']):
    dsn = dsn+A+'='+B+' '

command = ['goose', '-dir', migorig, 'postgres', dsn, 'status']

p = subprocess.Popen(command, stderr=subprocess.PIPE)
status = str(p.communicate()[1])


remigration = r'(\w{3} \w{3} \d{1,2} \d{1,2}:\d{1,2}:\d{1,2} \d{4}) -- ([\d\w_\.]+)'
m = re.findall(remigration, status, re.M)

for i in range(len(m)):
    m[i][0] = time.mktime(datetime.datetime.strptime(
        m[i][0], "%a %b %d %H:%M:%S %Y").timetuple())

delta = 0.001
for i in range(1, len(m)):
    if(int(m[i][0]) == m([i-1][0])):
        m[i][0] = m[i][0]+delta

for x in m:
    pass
