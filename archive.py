import shutil
import sys

print(sys.argv)

sqlFile = "schema"
folder = "./tables"
shutil.make_archive(sqlFile, 'zip', folder)
shutil.rmtree(folder)