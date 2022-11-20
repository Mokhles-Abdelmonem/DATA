from django.test import TestCase

# Create your tests here.



import os
import shutil
directorys = ["cleandata","collectdata","discoverdata","users"]
for dir in directorys:
    directory = f'{dir}/migrations'
    directory2 = f'{dir}/__pycache__'
    directory3 = f'{dir}/migrations/__pycache__'
    try:
        shutil.rmtree(directory2)
        shutil.rmtree(directory3)
    except:
        pass
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if not "__init__" in filename :
            if os.path.isfile(f):
                print(f)
                os.remove(f)

