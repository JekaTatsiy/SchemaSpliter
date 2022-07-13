import shutil

sqlFile = "schema"
folder = "./tables"
shutil.make_archive(sqlFile, 'zip', folder)
