import os
import glob

def remove_db_file():
    files = glob.glob('../../test.db')
    for f in files:
        os.remove(f)